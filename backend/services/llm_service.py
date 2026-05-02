import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key and api_key != "YOUR_GEMINI_API_KEY_HERE":
    genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.3,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=generation_config
)

def generate_final_notes(url: str) -> str:
    """
    Takes the YouTube URL and generates structured notes natively using Gemini.
    """
    prompt = f"""
    Please watch the following YouTube video and convert its content into structured study notes with:

    1. Summary
    2. Key Points (bullets)
    3. Important Concepts
    4. Examples (if any)
    
    Make it clear, concise, and student-friendly. Use Markdown formatting.
    
    Video URL:
    {url}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f"Failed to generate final notes: {str(e)}")
