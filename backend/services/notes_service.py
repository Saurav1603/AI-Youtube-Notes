from .transcript_service import extract_video_id, fetch_transcript
from .llm_service import generate_final_notes

def generate_notes_from_url(url: str) -> str:
    """
    Pipeline to generate structured notes from a YouTube URL.
    1. Extract Video ID
    2. Fetch Transcript
    3. Generate final structured notes directly from transcript (to save API limits)
    """
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL provided.")
    
    # Fetch transcript
    try:
        transcript_text = fetch_transcript(video_id)
    except Exception as e:
        raise ValueError(f"Could not retrieve transcript. Make sure the video has captions. Details: {str(e)}")
        
    # Pass the ENTIRE transcript to Gemini directly in one request
    # Gemini 2.5 Flash has a very large context window, so chunking isn't strictly necessary.
    final_notes = generate_final_notes(transcript_text)
    
    return final_notes
