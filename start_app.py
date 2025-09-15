#!/usr/bin/env python3
"""
Simple startup script for Hindi LLM Summarizer Pro
"""
import sys
import os
import subprocess

def main():
    print("🚀 Starting Hindi LLM Summarizer Pro...")
    
    # Check if we're in the right directory
    if not os.path.exists("app/main.py"):
        print("❌ Error: app/main.py not found. Please run from the project root.")
        return
    
    # Use the virtual environment Python
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    
    if not os.path.exists(venv_python):
        print("❌ Error: Virtual environment not found. Please run: python -m venv venv")
        return
    
    print("✅ Virtual environment found")
    print("🌐 Starting FastAPI server on http://localhost:8000")
    print("📱 Language selection: http://localhost:8000/")
    print("📊 Dashboard: http://localhost:8000/summarizer")
    print("\n" + "="*50)
    
    try:
        # Start the FastAPI server
        subprocess.run([
            venv_python, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
