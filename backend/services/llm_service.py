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

def summarize_chunk(chunk: str) -> str:
    """
    Summarizes a single chunk of text to extract key information.
    """
    prompt = f"""
    Please extract the key information, main points, and any important concepts or examples from the following transcript excerpt.
    Keep it concise but detailed enough to not lose context.
    
    Transcript Excerpt:
    {chunk}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing chunk: {str(e)}"

def generate_final_notes(combined_summaries: str) -> str:
    """
    Takes the combined summaries of all chunks and generates structured notes.
    """
    prompt = f"""
    Convert the following content into structured study notes with:

    1. Summary
    2. Key Points (bullets)
    3. Important Concepts
    4. Examples (if any)
    
    Make it clear, concise, and student-friendly. Use Markdown formatting.
    
    Content:
    {combined_summaries}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f"Failed to generate final notes: {str(e)}")
