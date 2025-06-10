from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from pytube import YouTube
from datetime import timedelta
import pdfplumber
import os
import yt_dlp

from summary import summarize_with_sumy  # Assuming you have this implemented

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the models properly
class YouTubeURL(BaseModel):
    url: HttpUrl

class VideoMetadata(BaseModel):
    title: str
    description: str
    publish_date: str
    duration: str
    views: int
    author: str
    thumbnail_url: str

import logging

import yt_dlp

@app.post("/extract", response_model=VideoMetadata)
def extract_video_data(video: YouTubeURL):
    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'format': 'best',
            'cookiefile': 'cookies.txt'  # Make sure this file exists and is valid
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(str(video.url), download=False)

        duration = str(timedelta(seconds=info.get("duration", 0)))

        return VideoMetadata(
            title=info.get("title", "N/A"),
            description=info.get("description", "N/A"),
            publish_date=info.get("upload_date", "N/A"),
            duration=duration,
            views=info.get("view_count", 0),
            author=info.get("uploader", "N/A"),
            thumbnail_url=info.get("thumbnail", "")
        )
    except Exception as e:
        logging.error(f"Error extracting video data: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to extract video data: {str(e)}")

@app.post("/extract-text/")
async def extract_text_from_pdf(file: UploadFile = File(...)):
    # Make sure upload folder exists
    os.makedirs("uploads", exist_ok=True)
    save_path = f"uploads/{file.filename}"

    # Save the uploaded PDF
    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)

    extracted_text = ""
    try:
        with pdfplumber.open(save_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:  # Make sure there's text on the page
                    extracted_text += text + "\n"
    except Exception as e:
        os.remove(save_path)
        raise HTTPException(status_code=400, detail=f"Failed to extract text from PDF: {str(e)}")

    # Count words from the extracted text
    words = extracted_text.split()
    word_count = len(words)
    summary = summarize_with_sumy(extracted_text)

    os.remove(save_path)  # Delete the file after processing

    return {"text": extracted_text, "word_count": word_count, "summary": summary}
