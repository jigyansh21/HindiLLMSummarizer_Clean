"""
Simple FastAPI application for MultiLanguage AI Text Summarizer
"""
from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, Literal
import asyncio
import os
import tempfile
import shutil
from pathlib import Path

from summarizer import SummarizerService
from pdf_utils import PDFProcessor
from youtube_utils import YouTubeProcessor

# Initialize FastAPI app
app = FastAPI(
    title="MultiLanguage AI Text Summarizer",
    description="Professional AI-powered text summarization in Hindi and English",
    version="2.0.0"
)

# Define base directory for robust path handling
BASE_DIR = Path(__file__).resolve().parent

# Mount static files
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Initialize services
summarizer_service = SummarizerService()
pdf_processor = PDFProcessor()
youtube_processor = YouTubeProcessor()

# Pydantic models
class SummarizeRequest(BaseModel):
    text: str
    language: Literal["hindi", "english"] = "hindi"
    summary_length: Literal["short", "medium", "long", "auto"] = "auto"

class SummarizeURLRequest(BaseModel):
    url: str
    language: Literal["hindi", "english"] = "hindi"
    summary_length: Literal["short", "medium", "long", "auto"] = "auto"

class SummarizePDFRequest(BaseModel):
    language: Literal["hindi", "english"] = "hindi"
    summary_length: Literal["short", "medium", "long", "auto"] = "auto"

class SummarizeYouTubeRequest(BaseModel):
    url: str
    language: Literal["hindi", "english"] = "hindi"
    summary_length: Literal["short", "medium", "long", "auto"] = "auto"

# Routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Language selection page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/summarizer", response_class=HTMLResponse)
async def summarizer_page(request: Request, language: str = "hindi"):
    """Main summarizer dashboard"""
    return templates.TemplateResponse("summarizer.html", {
        "request": request, 
        "language": language
    })

@app.get("/result", response_class=HTMLResponse)
async def result_page(request: Request, summary: str = "", title: str = "Summary", language: str = "hindi"):
    """Results page with summary display"""
    return templates.TemplateResponse("result.html", {
        "request": request,
        "summary": summary,
        "title": title,
        "language": language
    })

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "MultiLanguage AI Text Summarizer is running!"}

# API Endpoints
@app.post("/api/summarize/text")
async def summarize_text(request: SummarizeRequest):
    """Summarize raw text"""
    try:
        result = await summarizer_service.summarize_text(
            text=request.text,
            language=request.language,
            summary_length=request.summary_length
        )
        return {
            "success": True,
            "summary": result["summary"],
            "original_length": result["original_length"],
            "summary_length": result["summary_length"],
            "compression_ratio": result["compression_ratio"],
            "processing_time": result["processing_time"],
            "language": request.language
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/summarize/url")
async def summarize_url(request: SummarizeURLRequest):
    """Extract and summarize content from URL"""
    try:
        result = await summarizer_service.summarize_url(
            url=request.url,
            language=request.language,
            summary_length=request.summary_length
        )
        return {
            "success": True,
            "summary": result["summary"],
            "title": result["title"],
            "original_length": result["original_length"],
            "summary_length": result["summary_length"],
            "compression_ratio": result["compression_ratio"],
            "processing_time": result["processing_time"],
            "language": request.language
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/summarize/pdf")
async def summarize_pdf(
    file: UploadFile = File(...),
    language: str = Form("hindi"),
    summary_length: str = Form("auto")
):
    """Upload and summarize PDF content"""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            # Extract text from PDF
            extracted_text = await pdf_processor.extract_text(tmp_file_path)
            
            if not extracted_text.strip():
                raise HTTPException(status_code=400, detail="No text found in PDF")
            
            # Summarize the extracted text
            result = await summarizer_service.summarize_text(
                text=extracted_text,
                language=language,
                summary_length=summary_length
            )
            
            return {
                "success": True,
                "summary": result["summary"],
                "original_length": result["original_length"],
                "summary_length": result["summary_length"],
                "compression_ratio": result["compression_ratio"],
                "processing_time": result["processing_time"],
                "language": language,
                "filename": file.filename
            }
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/summarize/youtube")
async def summarize_youtube(request: SummarizeYouTubeRequest):
    """Extract transcript and summarize YouTube video"""
    try:
        result = await youtube_processor.summarize_video(
            url=request.url,
            language=request.language,
            summary_length=request.summary_length
        )
        return {
            "success": True,
            "summary": result["summary"],
            "title": result["title"],
            "original_length": result["original_length"],
            "summary_length": result["summary_length"],
            "compression_ratio": result["compression_ratio"],
            "processing_time": result["processing_time"],
            "language": request.language
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/export/pdf")
async def export_pdf(
    summary: str = Form(...),
    title: str = Form("Summary"),
    language: str = Form("hindi")
):
    """Export summary as PDF"""
    try:
        pdf_path = await summarizer_service.export_pdf(
            summary=summary,
            title=title,
            language=language
        )
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"{title.replace(' ', '_')}.pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/export/word")
async def export_word(
    summary: str = Form(...),
    title: str = Form("Summary"),
    language: str = Form("hindi")
):
    """Export summary as Word document"""
    try:
        doc_path = await summarizer_service.export_word(
            summary=summary,
            title=title,
            language=language
        )
        return FileResponse(
            doc_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=f"{title.replace(' ', '_')}.docx"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/export/markdown")
async def export_markdown(
    summary: str = Form(...),
    title: str = Form("Summary"),
    language: str = Form("hindi")
):
    """Export summary as Markdown"""
    try:
        md_path = await summarizer_service.export_markdown(
            summary=summary,
            title=title,
            language=language
        )
        return FileResponse(
            md_path,
            media_type="text/markdown",
            filename=f"{title.replace(' ', '_')}.md"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

