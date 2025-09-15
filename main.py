#!/usr/bin/env python3
"""
MultiLanguage AI Text Summarizer
Main entry point for the application
"""

import sys
import os
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the FastAPI app
from src.api.main import app

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting MultiLanguage AI Text Summarizer...")
    print("📱 Language selection: http://127.0.0.1:8000/")
    print("📊 Dashboard: http://127.0.0.1:8000/summarizer")
    print("🔍 Health check: http://127.0.0.1:8000/health")
    print("\n" + "="*50)
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
