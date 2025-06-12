from fastapi import APIRouter, UploadFile, File, HTTPException, status
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
import xml.etree.ElementTree
from datetime import timedelta
import yt_dlp
import pdfplumber
import os
import logging
import google.generativeai as genai

from models import ChatRequest, ChatResponse, YouTubeURL, VideoMetadata
from base import extract_video_id
from summary import summarize_with_sumy

router = APIRouter()


@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat_with_bot(request: ChatRequest):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(request.prompt)
        return ChatResponse(text=response.text)
    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error communicating with AI model: {e}"
        )


@router.post("/extract", response_model=VideoMetadata)
async def extract_video_data(video: YouTubeURL):
    video_url = str(video.url)
    video_id = extract_video_id(video_url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL.")

    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'format': 'best',
            'cookiefile': 'cookies.txt'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
        
        metadata = VideoMetadata(
            title=info.get("title", "N/A"),
            description=info.get("description", "N/A"),
            publish_date=info.get("upload_date", "N/A"),
            duration=str(timedelta(seconds=info.get("duration", 0))),
            views=info.get("view_count", 0),
            author=info.get("uploader", "N/A"),
            thumbnail_url=info.get("thumbnail", "")
        )
        metadata.summary = summarize_with_sumy(metadata.description)

    except Exception as e:
        logging.error(f"yt-dlp error: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Metadata extraction failed: {e}")

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = None
        try:
            transcript = transcript_list.find_transcript(['en'])
        except NoTranscriptFound:
            for tr in transcript_list:
                if tr.is_generated:
                    transcript = tr
                    break
            if not transcript and transcript_list:
                transcript = transcript_list[0]

        if transcript:
            full_transcript_data = transcript.fetch()
            metadata.transcript = " ".join([entry['text'] for entry in full_transcript_data])
            metadata.transcript_available = True

    except (NoTranscriptFound, TranscriptsDisabled):
        metadata.transcript_available = False
    except Exception as e:
        logging.error(f"Transcript fetch error: {e}")
        metadata.transcript_available = False

    return metadata


@router.post("/extract-text/")
async def extract_text_from_pdf(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    save_path = f"uploads/{file.filename}"

    try:
        with open(save_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File save error: {e}")

    extracted_text = ""
    try:
        with pdfplumber.open(save_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
    except Exception as e:
        os.remove(save_path)
        raise HTTPException(status_code=400, detail=f"Text extraction failed: {e}")

    word_count = len(extracted_text.split())
    summary = summarize_with_sumy(extracted_text)

    try:
        os.remove(save_path)
    except Exception as e:
        logging.warning(f"Failed to delete temp PDF: {e}")

    return {
        "text": extracted_text,
        "word_count": word_count,
        "summary": summary
    }
