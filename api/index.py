"""
Vercel WSGI Entry Point for MultiLanguage AI Text Summarizer
This file serves as the entry point for Vercel deployment
"""

import sys
import os
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Import the FastAPI app
from src.api.main import app

# Export the app for Vercel
handler = app
