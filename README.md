# Hindi LLM Summarizer

A powerful Streamlit-based web application that uses machine learning to generate Hindi summaries from various input sources including manual text, URLs, and PDF documents.

## 🌟 Features

- **Multiple Input Sources**:
  - Manual Hindi text input
  - URL article extraction
  - PDF document processing
- **Flexible Summary Lengths**:
  - Short (~15-25 words)
  - Medium (~30-50 words) 
  - Long (~80+ words)
- **PDF Export**: Download summaries as PDF with proper Hindi font support
- **Real-time Processing**: Fast summarization using pre-trained multilingual models
- **User-friendly Interface**: Clean, intuitive Streamlit web interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd HindiLLMSummarizer_Clean
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

## 📋 Requirements

The application requires the following Python packages:

- `streamlit==1.35.0` - Web application framework
- `transformers==4.41.1` - Hugging Face transformers for ML models
- `PyMuPDF==1.24.5` - PDF processing library
- `newspaper3k==0.2.8` - Article extraction from URLs
- `lxml==5.2.1` - XML/HTML processing

## 🎯 Usage

### 1. Manual Text Input
- Select "Manual Hindi Text" option
- Type or paste your Hindi text (max 1200 words)
- Choose your preferred summary length
- Click "Generate Hindi Summary"

### 2. URL Article Extraction
- Select "Enter Article URL" option
- Paste the URL of the article you want to summarize
- The app will automatically extract the content
- Choose summary length and generate

### 3. PDF Document Processing
- Select "Upload PDF" option
- Upload a PDF file (max 20 pages recommended)
- The app will extract text from the PDF
- Generate your summary

### 4. Export Summary
- After generating a summary, click "Download Summary as PDF"
- The PDF will be generated with proper Hindi font support

## 🔧 Technical Details

### Model Information
- **Model**: `csebuetnlp/mT5_multilingual_XLSum`
- **Type**: Multilingual T5 (Text-to-Text Transfer Transformer)
- **Capabilities**: Supports multiple languages including Hindi
- **Architecture**: Encoder-decoder transformer model

### Key Components

1. **Text Processing**:
   - PDF text extraction using PyPDF2
   - URL content extraction using newspaper3k
   - Text preprocessing and tokenization

2. **Summarization Engine**:
   - Pre-trained multilingual T5 model
   - Configurable summary lengths
   - Beam search decoding for quality summaries

3. **PDF Generation**:
   - Custom PDF creation with Hindi font support
   - Uses Noto Sans Devanagari font for proper rendering
   - Multi-line text handling

## 📁 Project Structure

```
HindiLLMSummarizer_Clean/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── fonts/                # Hindi font files
│   ├── NotoSansDevanagari-Regular.ttf
│   ├── NotoSansDevanagari-Regular.pkl
│   └── NotoSansDevanagari-Regular.cw127.pkl
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🛠️ Configuration

### Environment Variables
The application sets the following environment variable for optimal performance:
- `PYTORCH_JIT=0` - Disables PyTorch JIT compilation for Windows compatibility

### Font Configuration
The application uses Noto Sans Devanagari font for proper Hindi text rendering in PDFs. The font files are included in the `fonts/` directory.

## 🚨 Troubleshooting

### Common Issues

1. **Model Loading Issues**:
   - Ensure you have a stable internet connection for initial model download
   - The model will be cached locally after first download

2. **PDF Generation Errors**:
   - Verify that font files are present in the `fonts/` directory
   - Check file permissions for the fonts folder

3. **Memory Issues**:
   - For large PDFs, consider reducing the number of pages
   - Close other applications to free up memory

4. **URL Extraction Failures**:
   - Some websites may block automated content extraction
   - Try different URLs or use manual text input as alternative

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Jigyansh**  
ECE Undergraduate  
Thapar Institute of Engineering Technology

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) for the pre-trained models
- [Streamlit](https://streamlit.io/) for the web framework
- [Google Fonts](https://fonts.google.com/) for the Noto Sans Devanagari font

## 📞 Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.

---

**Note**: This application is designed for educational and research purposes. Please ensure you have the right to process and summarize the content you input into the application.
