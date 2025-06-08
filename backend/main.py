from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import os

from summary import summarize_with_sumy

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract-text/")
async def extract_text_from_pdf(file: UploadFile = File(...)):
    save_path = f"uploads/{file.filename}"

    # Save the uploaded PDF
    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)

    extracted_text = ""
    with pdfplumber.open(save_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:  # Make sure there's text on the page
                extracted_text += text + "\n"

    # Count words from the extracted text
    words = extracted_text.split()
    word_count = len(words)
    summary = summarize_with_sumy(extracted_text)
    os.remove(save_path)  # Delete the file after processing

    return {"text": extracted_text, "word_count": word_count,"summary":summary}