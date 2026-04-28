import re
import requests
import html
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

def fetch_transcript_innertube(video_id: str) -> str:
    """
    Uses YouTube's InnerTube API mimicking an older Android client.
    This bypasses the web HTML 'Confirm you're not a bot' blocks natively.
    """
    url = "https://www.youtube.com/youtubei/v1/player"
    payload = {
        "context": {
            "client": {
                "clientName": "ANDROID",
                "clientVersion": "17.31.35",
                "androidSdkVersion": 30,
                "userAgent": "com.google.android.youtube/17.31.35 (Linux; U; Android 11; en_US; Pixel 5 Build/RQ3A.210805.001.A1; gzip)"
            }
        },
        "videoId": video_id
    }
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "com.google.android.youtube/17.31.35 (Linux; U; Android 11; en_US; Pixel 5 Build/RQ3A.210805.001.A1; gzip)"
    }
    
    res = requests.post(url, json=payload, headers=headers, timeout=15)
    if res.status_code != 200:
        raise Exception("InnerTube API blocked or unavailable.")
        
    data = res.json()
    playability = data.get("playabilityStatus", {}).get("status", "")
    if playability == "ERROR":
        raise Exception("Video is unavailable or requires age verification.")
        
    caption_tracks = data.get("captions", {}).get("playerCaptionsTracklistRenderer", {}).get("captionTracks", [])
    if not caption_tracks:
        raise Exception("No caption tracks found via InnerTube Android Bypass.")
        
    en_track = None
    for track in caption_tracks:
        lang_code = track.get("languageCode", "").lower()
        if "en" in lang_code:
            en_track = track
            # prioritize manual english over auto-generated 'a.en'
            if "a.en" not in track.get("vssId", ""):
                break
                
    if not en_track:
        raise Exception("No English tracks found inside InnerTube response.")
        
    track_url = en_track["baseUrl"]
    xml_res = requests.get(track_url, timeout=15)
    if xml_res.status_code != 200:
        raise Exception("Failed to fetch InnerTube XML track.")
        
    # Extract text content from XML
    texts = re.findall(r'<text[^>]*>(.*?)</text>', xml_res.text)
    texts = [html.unescape(t).replace("\n", " ") for t in texts]
    
    final_text = " ".join(texts).strip()
    if not final_text:
        raise Exception("Parsed empty transcript directly from InnerTube")
        
    return final_text

def fetch_transcript(video_id: str) -> str:
    """
    Fetches the transcript by defaulting to the mobile-mimic InnerTube bypass directly.
    Most Cloud IPs are blocked heavily, so direct bypass is prioritizing.
    """
    try:
        print("Attempting InnerTube Android API payload...")
        return fetch_transcript_innertube(video_id)
    except Exception as e1:
        print(f"InnerTube Bypass failed: {str(e1)}")
        
        # Fallback to standard scraper (in case we're on local/clean IP network)
        try:
            print("Falling back to standard YouTubeTranscriptApi...")
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
        except Exception as e2:
            raise Exception(f"All extraction methods exhausted. Cloud server IP is likely permanently blacklisted. Errors: [Bypass: {str(e1)}] [Scraper: {str(e2)}]")
