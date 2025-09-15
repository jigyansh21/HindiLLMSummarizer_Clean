#!/usr/bin/env python3
"""
Simple script to run the FastAPI application
"""
import uvicorn
import os
import sys

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

if __name__ == "__main__":
    print("🚀 Starting Hindi LLM Summarizer Pro (FastAPI)")
    print("📍 Server will be available at: http://localhost:8000")
    print("🌐 Language selection: http://localhost:8000/")
    print("📊 Dashboard: http://localhost:8000/summarizer")
    print("\n" + "="*50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
