#!/usr/bin/env python3
"""
Test script for Hindi LLM Summarizer Pro
"""
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    try:
        import main
        print("✅ FastAPI app imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI app import failed: {e}")
        return False
    
    try:
        import summarizer
        print("✅ SummarizerService imported successfully")
    except ImportError as e:
        print(f"❌ SummarizerService import failed: {e}")
        return False
    
    try:
        import pdf_utils
        print("✅ PDFProcessor imported successfully")
    except ImportError as e:
        print(f"❌ PDFProcessor import failed: {e}")
        return False
    
    try:
        import youtube_utils
        print("✅ YouTubeProcessor imported successfully")
    except ImportError as e:
        print(f"❌ YouTubeProcessor import failed: {e}")
        return False
    
    return True

def test_templates():
    """Test if template files exist"""
    print("\n📄 Testing template files...")
    
    template_files = [
        "app/templates/index.html",
        "app/templates/summarizer.html", 
        "app/templates/result.html"
    ]
    
    for template in template_files:
        if os.path.exists(template):
            print(f"✅ {template} exists")
        else:
            print(f"❌ {template} missing")
            return False
    
    return True

def test_static_files():
    """Test if static files exist"""
    print("\n🎨 Testing static files...")
    
    static_files = [
        "app/static/styles.css"
    ]
    
    for static_file in static_files:
        if os.path.exists(static_file):
            print(f"✅ {static_file} exists")
        else:
            print(f"❌ {static_file} missing")
            return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Hindi LLM Summarizer Pro - Test Suite")
    print("=" * 50)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test templates
    if not test_templates():
        all_passed = False
    
    # Test static files
    if not test_static_files():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! The application is ready to run.")
        print("\n🚀 To start the application:")
        print("   python run_fastapi.py")
        print("\n🌐 Then visit: http://localhost:8000")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    main()
