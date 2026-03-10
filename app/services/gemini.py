from google import genai
from app.core.config import settings

def get_gemini_response(prompt: str) -> str:
    if not settings.GEMINI_API_KEY:
        return "Gemini API Key not configured."

    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return f"Error contacting Gemini: {str(e)}"
