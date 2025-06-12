import re
import logging
import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyC7xOrTyLXMLRHZ9GGPlQ4VabAXQvOCgGA"

def configure_gemini():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        logging.error(f"Error configuring Gemini API: {e}")

def extract_video_id(url: str):
    match = re.search(r'(?:v=|youtu\.be/|embed/|shorts/|watch\?v=|&v=)([^"&?\/\s]{11})', url)
    return match.group(1) if match else None
