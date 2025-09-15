# Hindi LLM Summarizer Pro - FastAPI Version

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
# Option 1: Using the startup script
python run_fastapi.py

# Option 2: Direct uvicorn
cd app
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Access the Application
- **Language Selection**: http://localhost:8000/
- **Main Dashboard**: http://localhost:8000/summarizer
- **API Documentation**: http://localhost:8000/docs

## 🎯 Features

### ✅ Backend (FastAPI)
- **Async endpoints** for high performance
- **4 input types**: Text, URL, PDF, YouTube
- **Language support**: Hindi and English
- **Summary lengths**: Short, Medium, Long, Auto
- **Export options**: PDF, Word, Markdown

### ✅ Frontend (Jinja2 + TailwindCSS)
- **3 pages**: Language selection, Dashboard, Results
- **Responsive design** with TailwindCSS
- **Professional UI/UX** with smooth animations
- **Dark/Light mode** support

### ✅ API Endpoints
- `POST /api/summarize/text` - Summarize raw text
- `POST /api/summarize/url` - Extract and summarize URL
- `POST /api/summarize/pdf` - Upload and summarize PDF
- `POST /api/summarize/youtube` - Extract transcript and summarize
- `POST /api/export/pdf` - Export as PDF
- `POST /api/export/word` - Export as Word
- `POST /api/export/markdown` - Export as Markdown

## 🏗️ Project Structure
```
app/
├── main.py              # FastAPI application
├── summarizer.py        # Core AI summarization logic
├── pdf_utils.py         # PDF processing utilities
├── youtube_utils.py     # YouTube transcript extraction
├── templates/           # Jinja2 HTML templates
│   ├── index.html       # Language selection page
│   ├── summarizer.html  # Main dashboard
│   └── result.html      # Results display
├── static/              # Static assets
│   └── styles.css       # Custom CSS
└── requirements.txt     # Python dependencies
```

## 🔧 Configuration

### Environment Variables
- `PYTORCH_JIT=0` - Disable PyTorch JIT for Windows compatibility

### Font Support
- Hindi fonts are located in `../fonts/NotoSansDevanagari-Regular.ttf`
- Automatic fallback to Arial if Hindi font not found

## 🎨 UI Features

### Language Selection Page
- Beautiful gradient background
- Hindi and English language cards
- Feature overview with icons
- Smooth hover animations

### Main Dashboard
- Tabbed interface (Text, URL, PDF, YouTube)
- Real-time word count and validation
- Summary length selection
- Processing statistics sidebar
- Professional loading animations

### Results Page
- Styled summary display
- Quality metrics and statistics
- Multiple export options
- Copy to clipboard functionality
- Share functionality

## 🚀 Performance

- **Async processing** for better performance
- **Model caching** to avoid reloading
- **Chunked processing** for large texts
- **Progress tracking** with real-time updates
- **Error handling** with graceful fallbacks

## 📱 Responsive Design

- **Mobile-first** approach
- **TailwindCSS** for consistent styling
- **Smooth animations** and transitions
- **Touch-friendly** interface elements

## 🔒 Security

- **Input validation** on all endpoints
- **File type validation** for uploads
- **Size limits** for PDFs and text
- **Error handling** without exposing internals

## 🎯 Interview Ready

This implementation demonstrates:
- **Modern FastAPI** with async/await
- **Clean architecture** with separation of concerns
- **Professional UI/UX** with TailwindCSS
- **Comprehensive error handling**
- **Documentation** and type hints
- **Scalable design** patterns

Perfect for showcasing full-stack Python development skills!
