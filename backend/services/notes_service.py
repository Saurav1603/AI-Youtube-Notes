import re
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

def generate_notes_from_url(url: str) -> str:
    """
    Pipeline to generate structured notes from a YouTube URL.
    """
    if not url or ("youtube.com" not in url and "youtu.be" not in url):
        raise ValueError("Invalid YouTube URL provided.")
    
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Could not extract video ID from the provided URL.")
        
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
        
    except Exception as e:
        raise ValueError(f"Could not retrieve transcript for this video. Error: {str(e)}")
    
    # Pass the full transcript text to Gemini
    final_notes = generate_final_notes(full_text)
    
    return final_notes
