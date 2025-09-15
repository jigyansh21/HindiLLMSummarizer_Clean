#!/usr/bin/env python3
"""
Working startup script for Hindi LLM Summarizer Pro
"""
import sys
import os
import subprocess
from pathlib import Path

def main():
    print("🚀 Starting Hindi LLM Summarizer Pro...")
    
    # Change to app directory
    app_dir = Path(__file__).parent / "app"
    os.chdir(app_dir)
    
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Check if files exist
    if not os.path.exists("simple_main.py"):
        print("❌ Error: simple_main.py not found")
        return
    
    if not os.path.exists("templates/index.html"):
        print("❌ Error: templates/index.html not found")
        return
    
    if not os.path.exists("static/styles.css"):
        print("❌ Error: static/styles.css not found")
        return
    
    print("✅ All files found")
    
    # Use the virtual environment Python
    venv_python = os.path.join("..", "venv", "Scripts", "python.exe")
    
    if not os.path.exists(venv_python):
        print("❌ Error: Virtual environment not found")
        return
    
    print("✅ Virtual environment found")
    print("🌐 Starting FastAPI server on http://127.0.0.1:8000")
    print("📱 Language selection: http://127.0.0.1:8000/")
    print("📊 Dashboard: http://127.0.0.1:8000/summarizer")
    print("🔍 Health check: http://127.0.0.1:8000/health")
    print("\n" + "="*50)
    
    try:
        # Start the FastAPI server
        subprocess.run([
            venv_python, "-m", "uvicorn", 
            "simple_main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
