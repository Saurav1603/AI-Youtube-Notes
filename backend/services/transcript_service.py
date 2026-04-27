import re
import yt_dlp
import requests
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url: str) -> str:
    """
    Extracts the YouTube video ID from a given URL.
    Handles standard youtube.com and youtu.be URLs.
    """
    regex = r"(?:v=|\/|youtu\.be\/|v\/|embed\/)([0-9A-Za-z_-]{11})"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None

def clean_vtt(vtt_text: str) -> str:
    """Removes WEBVTT metadata, styling, and timestamps from a raw .vtt file."""
    lines = vtt_text.split('\n')
    cleaned = []
    for line in lines:
        if line.startswith('WEBVTT') or '-->' in line or line.startswith('Kind:') or line.startswith('Language:') or line.startswith('Style:'):
            continue
        line = re.sub(r'<[^>]*>', '', line)
        line = re.sub(r'align:start position:\d+%', '', line)
        if line.strip().isdigit():
            continue
        if line.strip() and "Subscribe" not in line:
            cleaned.append(line.strip())
    
    # Remove duplicate consecutive lines
    final_cleaned = []
    for p in cleaned:
        if not final_cleaned or final_cleaned[-1] != p:
            final_cleaned.append(p)
            
    return " ".join(final_cleaned).replace("\n", " ").strip()

def fallback_fetch_with_ytdlp(url: str) -> str:
    """Uses yt-dlp to bypass IP bans by extracting the direct VTT subtitle URL."""
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        subs = info.get('requested_subtitles')
        if not subs or 'en' not in subs:
            raise Exception("No english captions found through yt-dlp fallback either.")
            
        sub_url = subs['en']['url']
        response = requests.get(sub_url)
        if response.status_code != 200:
            raise Exception("Failed to fetch subtitle file natively.")
            
        return clean_vtt(response.text)

def fetch_transcript(video_id: str) -> str:
    """
    Fetches the transcript natively using youtube-transcript-api.
    If blocked by YouTube Cloud IP ban logic, auto-reroutes to yt-dlp mobile-spoofing engine.
    """
    try:
        try:
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        except AttributeError:
            api = YouTubeTranscriptApi()
            transcript_list = api.list(video_id)
            transcript_data = transcript_list.find_transcript(['en']).fetch()

        text_parts = []
        for item in transcript_data:
            if isinstance(item, dict) and 'text' in item:
                text_parts.append(item['text'])
            elif hasattr(item, 'text'):
                text_parts.append(item.text)
                
        if not text_parts:
            raise Exception("No transcript items parsed.")
            
        return " ".join(text_parts).replace("\n", " ").strip()
        
    except Exception as e:
        error_msg = str(e).lower()
        if "could not retrieve a transcript" in error_msg or "blocked" in error_msg or "ip" in error_msg:
            print("Native API IP-Blocked. Booting yt-dlp fallback protocol...")
            return fallback_fetch_with_ytdlp(f"https://www.youtube.com/watch?v={video_id}")
        else:
            print("Native API failed, attempting immediate fallback to yt-dlp...")
            return fallback_fetch_with_ytdlp(f"https://www.youtube.com/watch?v={video_id}")
