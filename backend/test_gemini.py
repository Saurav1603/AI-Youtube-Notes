import os
import google.generativeai as genai
from dotenv import load_dotenv
import traceback

load_dotenv()
print("Starting Gemini test...")
try:
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("ERROR: API key not found")
        exit(1)
        
    genai.configure(api_key=api_key)
    
    # The llm_service uses gemini-2.5-flash, let's test it directly
    model_name = "gemini-2.5-flash"
    print(f"Testing {model_name}...")
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Say hello in exactly one word.")
    print("API RESPONSE:", response.text.strip())
    print("SUCCESS")
except Exception as e:
    print("FAILED with Exception:")
    traceback.print_exc()
