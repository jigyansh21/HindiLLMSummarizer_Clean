#!/usr/bin/env python3
"""
Simple startup script for MultiLanguage AI Text Summarizer
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("🚀 Starting MultiLanguage AI Text Summarizer...")
    print("📁 Working directory:", os.getcwd())
    
    # Check if main.py exists
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found")
        return
    
    print("✅ main.py found")
    print("🌐 Starting FastAPI server on http://127.0.0.1:8000")
    print("📱 Language selection: http://127.0.0.1:8000/")
    print("📊 Dashboard: http://127.0.0.1:8000/summarizer")
    print("🔍 Health check: http://127.0.0.1:8000/health")
    print("\n" + "="*50)
    
    try:
        # Start the FastAPI server
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
