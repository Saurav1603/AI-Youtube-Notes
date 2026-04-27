from youtube_transcript_api import YouTubeTranscriptApi
import re

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

def fetch_transcript(video_id: str) -> str:
    """
    Fetches the transcript for a given video ID using youtube-transcript-api.
    Combines the transcript into a single string resiliently.
    """
    try:
        try:
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        except AttributeError:
            api = YouTubeTranscriptApi()
            if hasattr(api, 'list'):
                transcript_list = api.list(video_id)
                try:
                    transcript_data = transcript_list.find_transcript(['en']).fetch()
                except Exception:
                    # fallback to first available
                    transcript_data = list(transcript_list)[0].fetch()
            elif hasattr(api, 'fetch'):
                transcript_data = api.fetch(video_id)
            else:
                raise Exception("Unknown YouTubeTranscriptApi format")
                
        # Handle formatting
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
        raise Exception(f"Failed to fetch transcript: {str(e)}")
