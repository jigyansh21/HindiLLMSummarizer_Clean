"""
FastAPI Backend for MultiLanguage AI Text Summarizer
Modern, async API with support for Text, URL, PDF, and YouTube summarization
"""

from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Literal
import os
import tempfile
import shutil
from pathlib import Path

# Import our modules
from src.core.summarizer import SummarizerService
from src.utils.pdf_utils import PDFProcessor
from src.utils.youtube_utils import YouTubeProcessor

# Initialize FastAPI app
app = FastAPI(
    title="MultiLanguage AI Text Summarizer",
    description="Professional AI-powered text summarization in Hindi and English",
    version="2.0.0"
)

# Define base directory for robust path handling
BASE_DIR = Path(__file__).parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# Ensure directories exist
TEMPLATES_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)

# Setup templates and static files
print(f"Templates directory: {TEMPLATES_DIR}")
print(f"Templates exists: {TEMPLATES_DIR.exists()}")
print(f"Templates contents: {list(TEMPLATES_DIR.glob('*.html')) if TEMPLATES_DIR.exists() else 'Directory not found'}")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Initialize services
summarizer_service = SummarizerService()
pdf_processor = PDFProcessor()
youtube_processor = YouTubeProcessor()

# Pydantic models for request validation
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

# Web Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Language selection page"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "MultiLanguage AI Text Summarizer"
    })

@app.get("/summarizer", response_class=HTMLResponse)
async def summarizer_dashboard(request: Request, language: str = "hindi"):
    """Main summarizer dashboard"""
    return templates.TemplateResponse("summarizer.html", {
        "request": request,
        "language": language,
        "title": "Summarizer Dashboard"
    })

@app.get("/result", response_class=HTMLResponse)
async def result_page(request: Request, summary: str, title: str = "Summary", language: str = "hindi"):
    """Results display page"""
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
        return result
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
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/summarize/pdf")
async def summarize_pdf(
    file: UploadFile = File(...),
    language: str = Form("hindi"),
    summary_length: str = Form("auto")
):
    """Upload and summarize PDF file"""
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name
        
        try:
            # Extract text from PDF
            text = await pdf_processor.extract_text(temp_path)
            
            # Summarize the text
            result = await summarizer_service.summarize_text(
                text=text,
                language=language,
                summary_length=summary_length
            )
            
            # Add file information
            result["filename"] = file.filename
            result["file_type"] = "PDF"
            
            return result
            
        finally:
            # Clean up temporary file
            os.unlink(temp_path)
            
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
        return result
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
