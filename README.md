# Hindi LLM Summarizer Pro

A powerful web application for summarizing text content in both Hindi and English using advanced AI models and extractive summarization techniques. The application supports multiple input sources including manual text, URLs, PDF files, and YouTube videos.

## ✨ Features

### 🌐 Multi-Language Support
- **Hindi & English** summarization
- Automatic language detection
- Language-specific processing

### 📝 Multiple Input Sources
- **Manual Text Input** - Direct text entry with word/character limits
- **URL Processing** - Extract and summarize content from web pages
- **PDF Documents** - Upload and process PDF files
- **YouTube Videos** - Extract transcripts and generate summaries

### 🎯 Smart Summarization
- **Extractive Summarization** - Advanced sentence selection algorithm
- **Multiple Length Options**:
  - Short (25% of original)
  - Medium (40% of original) 
  - Long (60% of original)
  - Auto (intelligent length selection)
- **Dynamic Word Targeting** - Optimized for different content lengths

### 🎨 Modern UI/UX
- **Dark/Light Theme Toggle** - Seamless theme switching with persistence
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Hero Icons** - Beautiful, consistent iconography
- **Gradient Backgrounds** - Modern visual design
- **Real-time Statistics** - Processing stats and word counts

### 📤 Export Options
- **PDF Export** - Generate PDF summaries
- **Word Document** - Create .docx files
- **Markdown** - Export as .md files
- **Copy to Clipboard** - Quick text copying

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd HindiLLMSummarizer_Clean
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python run_app.py
   ```

6. **Open in browser**
   Navigate to `http://127.0.0.1:8000`

## 📋 Requirements

### Core Dependencies
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Transformers** - Hugging Face models
- **PyTorch** - Deep learning framework
- **NLTK** - Natural language processing
- **BeautifulSoup4** - Web scraping
- **PyMuPDF** - PDF processing
- **python-docx** - Word document generation
- **youtube-transcript-api** - YouTube transcript extraction

### Optional Dependencies
- **T5 Model** - For advanced summarization (auto-downloaded)
- **Font Tools** - For Devanagari font support

## 🏗️ Project Structure

```
HindiLLMSummarizer_Clean/
├── app/
│   ├── main.py                 # Main FastAPI application
│   ├── simple_main.py          # Simplified FastAPI app
│   ├── summarizer.py           # Core summarization logic
│   ├── pdf_utils.py            # PDF processing utilities
│   ├── youtube_utils.py        # YouTube transcript extraction
│   ├── templates/              # HTML templates
│   │   ├── index.html          # Language selection page
│   │   ├── summarizer.html     # Main dashboard
│   │   └── result.html         # Results display
│   ├── static/                 # Static assets
│   │   └── styles.css          # Custom CSS
│   └── requirements.txt        # Python dependencies
├── fonts/                      # Devanagari font files
├── run_app.py                  # Application launcher
├── requirements.txt            # Root dependencies
└── README.md                   # This file
```

## 🔧 Configuration

### Environment Variables
- No environment variables required
- All configuration is handled internally

### Model Configuration
- **T5 Model**: Automatically downloads on first use
- **Extractive Summarization**: Primary method for reliability
- **Language Models**: Optimized for Hindi and English

## 📖 Usage Guide

### 1. Language Selection
- Choose between Hindi or English
- Language affects processing and UI display
- Can be changed at any time

### 2. Text Summarization
1. Select "Text" tab
2. Enter your text (max 1,200 words)
3. Choose summary length
4. Click "Generate Summary"

### 3. URL Summarization
1. Select "URL" tab
2. Paste the webpage URL
3. Choose summary length
4. Click "Generate Summary"

### 4. PDF Summarization
1. Select "PDF" tab
2. Upload PDF file
3. Choose summary length
4. Click "Generate Summary"

### 5. YouTube Summarization
1. Select "YouTube" tab
2. Paste YouTube video URL
3. Choose summary length
4. Click "Generate Summary"

### 6. Export Options
- **PDF**: Download as PDF file
- **Word**: Download as .docx file
- **Markdown**: Download as .md file
- **Copy**: Copy to clipboard

## 🎨 Theme Customization

### Dark Mode
- Click the sun/moon icon in the top-right
- Theme preference is saved automatically
- Consistent across all pages

### Light Mode
- Clean, modern light theme
- High contrast for readability
- Professional appearance

## 🔍 API Endpoints

### Web Pages
- `GET /` - Language selection
- `GET /summarizer` - Main dashboard
- `GET /result` - Summary results

### API Endpoints
- `POST /api/summarize/text` - Text summarization
- `POST /api/summarize/url` - URL summarization
- `POST /api/summarize/pdf` - PDF summarization
- `POST /api/summarize/youtube` - YouTube summarization
- `POST /api/export/pdf` - PDF export
- `POST /api/export/word` - Word export
- `POST /api/export/markdown` - Markdown export

## 🛠️ Technical Details

### Summarization Algorithm
1. **Text Preprocessing** - Clean and normalize input
2. **Sentence Splitting** - Split into sentences (supports Hindi punctuation)
3. **Scoring** - Calculate sentence importance
4. **Selection** - Choose optimal sentences for summary
5. **Post-processing** - Format and polish output

### Language Support
- **Hindi**: Full Devanagari script support
- **English**: Standard Latin script
- **Mixed Content**: Handles bilingual text

### Performance
- **Fast Processing** - Optimized algorithms
- **Memory Efficient** - Handles large documents
- **Scalable** - Supports multiple concurrent users

## 🐛 Troubleshooting

### Common Issues

1. **YouTube videos not working**
   - Ensure video has captions/transcripts
   - Check internet connection
   - Try different video

2. **PDF processing fails**
   - Ensure PDF is not password protected
   - Check file size (max 10MB)
   - Verify PDF is not corrupted

3. **Theme not switching**
   - Clear browser cache
   - Check browser console for errors
   - Ensure JavaScript is enabled

4. **Model loading issues**
   - Check internet connection
   - Ensure sufficient disk space
   - Restart application

### Error Messages
- **"No transcript available"** - YouTube video lacks captions
- **"PDF processing failed"** - PDF file issues
- **"Text too long"** - Exceeded word limit
- **"Invalid URL"** - Malformed web address

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Hugging Face** - For transformer models
- **FastAPI** - For the web framework
- **Tailwind CSS** - For styling
- **Heroicons** - For beautiful icons
- **YouTube Transcript API** - For video processing

## 📞 Support

For support, issues, or feature requests:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation

## 🔄 Version History

### v2.0.0 (Current)
- ✅ Dark/Light theme toggle
- ✅ YouTube transcript processing
- ✅ Enhanced extractive summarization
- ✅ Improved UI/UX with Heroicons
- ✅ Better error handling
- ✅ Cross-page theme persistence

### v1.0.0
- ✅ Basic text summarization
- ✅ PDF processing
- ✅ URL content extraction
- ✅ Multi-language support

---

**Made with ❤️ for the Hindi and English speaking community**