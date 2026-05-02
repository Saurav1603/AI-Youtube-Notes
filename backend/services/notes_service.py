from .llm_service import generate_final_notes

def generate_notes_from_url(url: str) -> str:
    """
    Pipeline to generate structured notes from a YouTube URL natively via Gemini.
    """
    if not url or ("youtube.com" not in url and "youtu.be" not in url):
        raise ValueError("Invalid YouTube URL provided.")
    
    # Pass the ENTIRE URL to Gemini directly in one request
    final_notes = generate_final_notes(url)
    
    return final_notes
