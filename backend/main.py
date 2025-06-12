from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import google.generativeai as genai

from base import configure_gemini
from routes import router

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure Gemini
configure_gemini()

# Create FastAPI app
app = FastAPI(
    title="Multimedia Extractor and Summarizer",
    description="API for extracting YouTube video metadata and text from PDFs, with summarization.",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Update as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)
