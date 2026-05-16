import re
import os
import glob
import tempfile
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
from .llm_service import generate_final_notes

def extract_video_id(url: str) -> str:
    """Extracts the YouTube video ID from a URL."""
    pattern = r'(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def extract_transcript_ytdlp(video_id: str) -> str:
    """Fallback method using yt-dlp to bypass IP blocks."""
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
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_id])
                
            # Find the downloaded .vtt file
            vtt_files = glob.glob(os.path.join(temp_dir, '*.vtt'))
            if not vtt_files:
                raise ValueError("No subtitles found using fallback method.")
                
            # Read the first available subtitle file
            with open(vtt_files[0], 'r', encoding='utf-8') as f:
                vtt_content = f.read()
                
            # Simple cleanup of VTT tags and timestamps
            lines = vtt_content.split('\n')
            clean_lines = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('WEBVTT') and not line.startswith('Kind:') and not line.startswith('Language:') and '-->' not in line:
                    # Remove any styling tags like <c> etc.
                    line = re.sub(r'<[^>]+>', '', line)
                    clean_lines.append(line)
                    
            # Removing duplicate lines (very common in VTT auto-subs)
            unique_lines = []
            for line in clean_lines:
                if not unique_lines or unique_lines[-1] != line:
                    unique_lines.append(line)
                    
            return " ".join(unique_lines)
            
        except Exception as e:
            raise ValueError(f"Fallback extraction failed: {str(e)}")

def generate_notes_from_url(url: str) -> str:
    """
    Pipeline to generate structured notes from a YouTube URL.
    """
    if not url or ("youtube.com" not in url and "youtu.be" not in url):
        raise ValueError("Invalid YouTube URL provided.")
    
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Could not extract video ID from the provided URL.")
        
    full_text = ""
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        
        try:
            # Try to fetch English transcript first
            transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
        except NoTranscriptFound:
            # Fallback: get the first available transcript and try to translate it to English
            first_available = list(transcript_list)[0]
            if first_available.is_translatable:
                transcript = first_available.translate('en')
            else:
                transcript = first_available
                
        snippets = transcript.fetch()
        full_text = " ".join([snippet.text for snippet in snippets])
        
    except Exception as api_err:
        print(f"Primary API failed: {str(api_err)}. Falling back to yt-dlp...")
        try:
            full_text = extract_transcript_ytdlp(video_id)
        except Exception as fallback_err:
            raise ValueError(f"Could not retrieve transcript for this video. Primary error: {str(api_err)}. Fallback error: {str(fallback_err)}")
    
    # Pass the full transcript text to Gemini
    final_notes = generate_final_notes(full_text)
    
    return final_notes
