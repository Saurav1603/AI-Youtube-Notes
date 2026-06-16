import re
import os
import glob
import tempfile
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
from .llm_service import generate_final_notes
from faster_whisper import WhisperModel

def extract_video_id(url: str) -> str:
    """Extracts the YouTube video ID from a URL."""
    pattern = r'(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def extract_transcript_api(video_id: str) -> str:
    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)
    
    try:
        transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB', 'hi'])
    except NoTranscriptFound:
        first_available = list(transcript_list)[0]
        if first_available.is_translatable:
            transcript = first_available.translate('en')
        else:
            transcript = first_available
            
    snippets = transcript.fetch()
    return " ".join([snippet['text'] if isinstance(snippet, dict) else snippet.text for snippet in snippets])

def extract_transcript_ytdlp_subs(video_id: str) -> str:
    with tempfile.TemporaryDirectory() as temp_dir:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en', 'hi'],
            'subtitlesformat': 'vtt',
            'outtmpl': os.path.join(temp_dir, '%(id)s.%(ext)s'),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_id])
            
        vtt_files = glob.glob(os.path.join(temp_dir, '*.vtt'))
        if not vtt_files:
            raise ValueError("No subtitles found.")
            
        with open(vtt_files[0], 'r', encoding='utf-8') as f:
            vtt_content = f.read()
            
        lines = vtt_content.split('\n')
        clean_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('WEBVTT') and not line.startswith('Kind:') and not line.startswith('Language:') and '-->' not in line:
                line = re.sub(r'<[^>]+>', '', line)
                clean_lines.append(line)
                
        unique_lines = []
        for line in clean_lines:
            if not unique_lines or unique_lines[-1] != line:
                unique_lines.append(line)
                
        return " ".join(unique_lines)

def extract_transcript_whisper(video_id: str) -> str:
    with tempfile.TemporaryDirectory() as temp_dir:
        ydl_opts = {
            'quiet': True,
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(temp_dir, '%(id)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Check duration to prevent server timeouts during synchronous transcription
            info = ydl.extract_info(video_id, download=False)
            duration = info.get('duration', 0)
            if duration > 600:
                raise ValueError(f"Video duration ({duration}s) exceeds the 10-minute limit for synchronous audio transcription. Aborting to prevent 504 Gateway Timeout.")
                
            ydl.download([video_id])
            
        audio_files = glob.glob(os.path.join(temp_dir, '*.mp3'))
        if not audio_files:
            raise ValueError("Failed to download audio.")
            
        audio_path = audio_files[0]
        
        # Load faster-whisper model
        # Using "tiny" to minimize RAM usage for cloud deployments (prevents Out of Memory errors)
        model = WhisperModel("tiny", device="cpu", compute_type="int8")
        
        segments, _ = model.transcribe(audio_path, beam_size=5)
        text = " ".join([segment.text for segment in segments])
        
        # Audio file will be automatically deleted when TemporaryDirectory context exits
        if not text.strip():
            raise ValueError("Whisper transcribed empty text.")
            
        return text

def extract_metadata_fallback(video_id: str) -> str:
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_id, download=False)
        title = info.get('title', 'Unknown Title')
        desc = info.get('description', 'No description available.')
        channel = info.get('uploader', 'Unknown Channel')
        
        return f"Title: {title}\nChannel: {channel}\nDescription: {desc}"

def generate_notes_from_url(url: str) -> tuple[str, bool]:
    """
    Pipeline to generate structured notes from a YouTube URL.
    Returns (notes_text, is_metadata_fallback)
    """
    if not url or ("youtube.com" not in url and "youtu.be" not in url):
        raise ValueError("Invalid YouTube URL provided.")
    
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Could not extract video ID from the provided URL.")
        
    full_text = ""
    is_metadata_fallback = False
    
    # Level 1: API
    try:
        print("Attempting Level 1: YouTubeTranscriptApi")
        full_text = extract_transcript_api(video_id)
    except Exception as e1:
        print(f"Level 1 failed: {e1}")
        
        # Level 2: yt-dlp Subtitles
        try:
            print("Attempting Level 2: yt-dlp Subtitles")
            full_text = extract_transcript_ytdlp_subs(video_id)
        except Exception as e2:
            print(f"Level 2 failed: {e2}")
            
            # Level 3: Whisper Audio Transcription
            try:
                print("Attempting Level 3: Whisper Audio Transcription")
                full_text = extract_transcript_whisper(video_id)
            except Exception as e3:
                print(f"Level 3 failed: {e3}")
                
                # Level 4: Metadata Fallback
                try:
                    print("Attempting Level 4: Metadata Fallback")
                    full_text = extract_metadata_fallback(video_id)
                    is_metadata_fallback = True
                except Exception as e4:
                    print(f"Level 4 failed: {e4}")
                    raise ValueError("All extraction methods failed, including metadata extraction.")
    
    # Pass the full text to Gemini
    final_notes = generate_final_notes(full_text, is_metadata=is_metadata_fallback)
    
    return final_notes, is_metadata_fallback
