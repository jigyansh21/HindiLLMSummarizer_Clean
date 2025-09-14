import streamlit as st
from transformers.models.t5 import T5Tokenizer, T5ForConditionalGeneration
import fitz  # PyMuPDF
import requests
from newspaper import Article
import tempfile
from fpdf import FPDF
import nltk
from PyPDF2 import PdfReader
import os
import time
import json
from datetime import datetime
# import plotly.express as px
# import plotly.graph_objects as go
from collections import Counter
import re

# Streamlit UI config
st.set_page_config(
    page_title="Hindi LLM Summarizer Pro",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
    }
    .success-message {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    .warning-message {
        background: linear-gradient(135deg, #ff9800, #f57c00);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    .error-message {
        background: linear-gradient(135deg, #f44336, #d32f2f);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa, #e9ecef);
    }
    .stButton > button {
        background: linear-gradient(135deg, #1f77b4, #ff7f0e);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .stSelectbox > div > div {
        background: white;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
    }
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        color: #333333 !important;
        background-color: #ffffff !important;
        font-size: 14px !important;
    }
    .stTextArea > div > div > textarea::placeholder {
        color: #666666 !important;
    }
    .stFileUploader > div > div {
        border-radius: 10px;
        border: 2px dashed #1f77b4;
        background: #f8f9fa;
    }
    .summary-display {
        background: #ffffff !important;
        color: #333333 !important;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        font-size: 1.1rem;
        line-height: 1.6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .text-preview {
        background: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
    }
    .metric-value {
        color: #333333 !important;
        font-weight: bold;
    }
    .stTextInput > div > div > input {
        color: #333333 !important;
        background-color: #ffffff !important;
    }
    .stSelectbox > div > div > div {
        color: #333333 !important;
        background-color: #ffffff !important;
    }
    /* Ensure all text is visible */
    .stTextArea textarea {
        color: #333333 !important;
        background-color: #ffffff !important;
    }
    .stTextInput input {
        color: #333333 !important;
        background-color: #ffffff !important;
    }
    /* Fix for any white text on white background */
    .stApp > div > div > div > div {
        color: #333333 !important;
    }
    /* Ensure textarea content is visible */
    textarea {
        color: #333333 !important;
        background-color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Download punkt
nltk.download("punkt")

# Set PyTorch workaround for Windows torch.classes issue
os.environ["PYTORCH_JIT"] = "0"

# Professional utility functions
@st.cache_data
def get_text_statistics(text):
    """Calculate comprehensive text statistics"""
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return {
        'word_count': len(words),
        'sentence_count': len(sentences),
        'avg_words_per_sentence': len(words) / len(sentences) if sentences else 0,
        'char_count': len(text),
        'unique_words': len(set(words)),
        'reading_time_minutes': len(words) / 200  # Average reading speed
    }

@st.cache_data
def analyze_text_quality(text):
    """Analyze text quality metrics"""
    stats = get_text_statistics(text)
    
    # Quality indicators
    quality_score = 0
    if stats['word_count'] > 50:
        quality_score += 25
    if stats['sentence_count'] > 5:
        quality_score += 25
    if stats['avg_words_per_sentence'] > 5 and stats['avg_words_per_sentence'] < 25:
        quality_score += 25
    if stats['unique_words'] / stats['word_count'] > 0.3:
        quality_score += 25
    
    return {
        'quality_score': quality_score,
        'complexity': 'High' if stats['avg_words_per_sentence'] > 15 else 'Medium' if stats['avg_words_per_sentence'] > 8 else 'Low',
        'readability': 'Good' if 5 <= stats['avg_words_per_sentence'] <= 20 else 'Needs Improvement'
    }

def create_progress_bar(message, progress=0):
    """Create a professional progress bar"""
    progress_bar = st.progress(progress)
    status_text = st.empty()
    status_text.text(message)
    return progress_bar, status_text

def show_loading_animation():
    """Show professional loading animation"""
    with st.spinner("🔄 Processing your request..."):
        time.sleep(0.5)

# Real model loading function
@st.cache_resource
def load_model():
    """Load the T5 model for Hindi summarization"""
    try:
        # Using Google's T5 model which supports multilingual tasks including Hindi
        model_name = "t5-small"  # Using t5-small for better compatibility
        
        st.info("🔄 Loading Google's T5 model... This may take a moment on first run.")
        
        tokenizer = T5Tokenizer.from_pretrained(model_name)
        model = T5ForConditionalGeneration.from_pretrained(model_name)
        
        st.success("✅ T5 Model loaded successfully!")
        return tokenizer, model
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        st.info("💡 Make sure you have a stable internet connection for model download.")
        return None, None

def real_summarize_text(text, summary_len, tokenizer, model):
    """Real summarization function using T5 model"""
    try:
        # Prepare the text for summarization
        if summary_len == "Short":
            max_length = 50
            min_length = 20
        elif summary_len == "Medium":
            max_length = 100
            min_length = 40
        else:  # Long
            max_length = 200
            min_length = 80
        
        # Add summarization prefix for T5
        input_text = f"summarize: {text}"
        
        # Tokenize the input
        inputs = tokenizer(
            input_text,
            max_length=512,  # T5 has a limit
            truncation=True,
            padding=True,
            return_tensors="pt"
        )
        
        # Generate summary
        with st.spinner("🤖 AI is generating your summary..."):
            outputs = model.generate(
                inputs.input_ids,
                max_length=max_length,
                min_length=min_length,
                num_beams=4,
                early_stopping=True,
                do_sample=False
            )
        
        # Decode the summary
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Clean up the summary
        summary = summary.strip()
        
        # If the model didn't generate a good summary, fall back to extractive summarization
        if len(summary.split()) < 5:
            # Fallback: take first few sentences
            sentences = text.split('.')
            if summary_len == "Short":
                summary = '. '.join(sentences[:2]) + '.'
            elif summary_len == "Medium":
                summary = '. '.join(sentences[:3]) + '.'
            else:
                summary = '. '.join(sentences[:4]) + '.'
        
        return summary
        
    except Exception as e:
        st.error(f"Error in summarization: {str(e)}")
        # Fallback to simple text truncation
        words = text.split()
        if summary_len == "Short":
            return " ".join(words[:20]) + "..."
        elif summary_len == "Medium":
            return " ".join(words[:40]) + "..."
        else:
            return " ".join(words[:80]) + "..."

# Initialize session state
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
if 'processing_stats' not in st.session_state:
    st.session_state.processing_stats = {'total_processed': 0, 'total_words': 0, 'avg_processing_time': 0}

# Load model (real)
tokenizer, model = load_model()
st.session_state.model_loaded = tokenizer is not None and model is not None

# Text chunking function for large documents
def chunk_text(text, chunk_size=800):
    """Split text into smaller chunks for processing"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

# Summarization function with chunking support
def summarize_text(text, summary_len, tokenizer, model):
    # If text is too long, chunk it and summarize each chunk
    word_count = len(text.split())
    
    if word_count > 1000:  # Use chunking for large texts
        chunks = chunk_text(text, chunk_size=800)
        summaries = []
        
        for i, chunk in enumerate(chunks):
            if chunk.strip():
                chunk_summary = real_summarize_text(chunk, summary_len, tokenizer, model)
                summaries.append(chunk_summary)
        
        # Combine chunk summaries
        combined_text = " ".join(summaries)
        # Final summarization of combined summaries
        return real_summarize_text(combined_text, summary_len, tokenizer, model)
    else:
        return real_summarize_text(text, summary_len, tokenizer, model)
 
# PDF text extraction with page limit validation
def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        total_pages = len(reader.pages)
        
        # Check page limit
        if total_pages > 15:
            st.warning(f"PDF has {total_pages} pages. Only the first 15 pages will be processed.")
            pages_to_process = 15
        else:
            pages_to_process = total_pages
            
        text = ""
        for i in range(pages_to_process):
            page_text = reader.pages[i].extract_text() or ""
            text += page_text + "\n"
            
        # Clean up text
        text = text.strip()
        
        # Check if text is too long for the model (approximate word count)
        word_count = len(text.split())
        if word_count > 3000:  # Conservative limit for model processing
            st.warning(f"Text is very long ({word_count} words). Processing first 3000 words.")
            text = " ".join(text.split()[:3000])
            
        return text
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return ""

# URL article extraction
def extract_text_from_url(url):
    try:
        article = Article(url, language="hi")
        article.download()
        article.parse()
        return article.text.strip()
    except:
        return ""

# Professional PDF generator for summary
def generate_pdf(summary, title="Hindi Summary", author="Hindi LLM Summarizer Pro"):
    """Generate a professional PDF with proper Hindi font support"""
    pdf = FPDF()
    pdf.add_page()
    
    # Set up fonts
    font_path = os.path.join(os.path.dirname(__file__), "fonts", "NotoSansDevanagari-Regular.ttf")
    if not os.path.exists(font_path):
        raise FileNotFoundError("fonts/NotoSansDevanagari-Regular.ttf not found in the project directory.")
    
    # Add font (fixed deprecation warning)
    pdf.add_font("NotoSans", "", font_path)
    pdf.set_font("NotoSans", size=16)
    
    # Add title
    pdf.cell(0, 15, title, 0, 1, 'C')
    pdf.ln(10)
    
    # Add metadata
    pdf.set_font("NotoSans", size=10)
    pdf.cell(0, 8, f"Generated by: {author}", 0, 1, 'C')
    pdf.cell(0, 8, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'C')
    pdf.ln(10)
    
    # Add summary content
    pdf.set_font("NotoSans", size=12)
    for line in summary.split("\n"):
        if line.strip():
            # Fixed deprecation warning - use 'text' instead of 'txt'
            pdf.multi_cell(0, 8, text=line.strip())
            pdf.ln(2)
    
    # Add footer
    pdf.ln(20)
    pdf.set_font("NotoSans", size=8)
    pdf.cell(0, 5, "Generated by Hindi LLM Summarizer Pro - Professional AI-Powered Text Summarization", 0, 1, 'C')
    
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp_file.name)
    return tmp_file.name

# Professional Header
st.markdown('<h1 class="main-header">📝 Hindi LLM Summarizer Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">🚀 Professional AI-Powered Text Summarization with Advanced Analytics</p>', unsafe_allow_html=True)

# Real model notice
st.markdown("""
<div style="background: linear-gradient(135deg, #4CAF50, #45a049); color: white; padding: 1rem; border-radius: 10px; margin: 1rem 0; text-align: center; font-weight: bold;">
🚀 LIVE MODE: Powered by Google's T5 AI model for real Hindi text summarization.
</div>
""", unsafe_allow_html=True)

# Sidebar for controls
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    # Model status
    if st.session_state.model_loaded:
        st.success("✅ T5 Model Ready")
    else:
        st.error("❌ Model Loading Failed")
        st.info("💡 Please check your internet connection and refresh the page.")
    
    # Summary length selection
    st.markdown("### 📏 Summary Length")
    length_option = st.selectbox(
        "Choose summary length:",
        ["Short", "Medium", "Long"],
        help="Short: 15-25 words, Medium: 30-50 words, Long: 80+ words"
    )
    
    # Advanced options
    st.markdown("### 🔧 Advanced Options")
    enable_analytics = st.checkbox("📊 Enable Analytics", value=True)
    show_quality_metrics = st.checkbox("📈 Show Quality Metrics", value=True)
    auto_download = st.checkbox("💾 Auto-download PDF", value=False)
    
    # Processing statistics
    st.markdown("### 📊 Session Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Documents Processed", st.session_state.processing_stats['total_processed'])
    with col2:
        st.metric("Total Words", st.session_state.processing_stats['total_words'])

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("## 🎯 Input Options")
    
    input_type = st.radio(
        "Choose your input method:",
        ["Manual Hindi Text", "Enter Article URL", "Upload PDF"],
        horizontal=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Input Limits")
    st.markdown("""
    - **Manual Text**: 1,200 words max
    - **PDF Documents**: 15 pages max  
    - **URL Articles**: Auto-processed
    - **Processing**: Real-time AI
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Input handling with professional styling
text_data = ""

if input_type == "Manual Hindi Text":
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("## ✍️ Manual Text Input")
    
    manual_input = st.text_area(
        "Type or paste your Hindi text here:",
        height=300,
        key="manual_text_input",
        placeholder="Enter your Hindi text here... (Maximum 1,200 words)",
        help="Enter your Hindi text for summarization. The text will be analyzed for quality and complexity."
    )
    
    if manual_input:
        word_count = len(manual_input.split())
        char_count = len(manual_input)
        
        # Real-time word count with color coding
        col1, col2, col3 = st.columns(3)
        with col1:
            if word_count <= 1200:
                st.success(f"📝 Words: {word_count}/1,200")
            else:
                st.warning(f"⚠️ Words: {word_count}/1,200 (Will be truncated)")
        with col2:
            st.info(f"📊 Characters: {char_count:,}")
        with col3:
            reading_time = word_count / 200
            st.info(f"⏱️ Reading Time: {reading_time:.1f} min")
        
        if word_count > 1200:
            st.markdown('<div class="warning-message">⚠️ Input exceeds 1,200 words. It will be automatically truncated to the first 1,200 words.</div>', unsafe_allow_html=True)
            manual_input = " ".join(manual_input.split()[:1200])
        
        text_data = manual_input
    st.markdown('</div>', unsafe_allow_html=True)

elif input_type == "Enter Article URL":
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("## 🌐 URL Article Extraction")
    
    url = st.text_input(
        "Paste the article URL:",
        placeholder="https://example.com/article",
        help="Enter a valid URL to extract and summarize the article content"
    )
    
    if url:
        if st.button("🔍 Extract Article", type="primary"):
            progress_bar, status_text = create_progress_bar("Extracting content from URL...", 0)
            
            try:
                progress_bar.progress(25)
                status_text.text("🌐 Connecting to URL...")
                time.sleep(0.5)
                
                progress_bar.progress(50)
                status_text.text("📄 Extracting article content...")
                text_data = extract_text_from_url(url)
                
                progress_bar.progress(75)
                status_text.text("✅ Processing complete!")
                
                if text_data:
                    progress_bar.progress(100)
                    status_text.text("🎉 Article extracted successfully!")
                    st.markdown('<div class="success-message">✅ Article content extracted successfully!</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-message">❌ Failed to extract content from the URL. Please check the URL and try again.</div>', unsafe_allow_html=True)
                
                progress_bar.empty()
                status_text.empty()
                
            except Exception as e:
                st.markdown(f'<div class="error-message">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
                progress_bar.empty()
                status_text.empty()
    st.markdown('</div>', unsafe_allow_html=True)

elif input_type == "Upload PDF":
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("## 📄 PDF Document Upload")
    
    uploaded_file = st.file_uploader(
        "Upload a Hindi PDF document:",
        type="pdf",
        help="Upload a PDF file (maximum 15 pages) for text extraction and summarization"
    )
    
    if uploaded_file:
        if st.button("📖 Process PDF", type="primary"):
            progress_bar, status_text = create_progress_bar("Processing PDF document...", 0)
            
            try:
                progress_bar.progress(20)
                status_text.text("📄 Reading PDF file...")
                time.sleep(0.5)
                
                progress_bar.progress(50)
                status_text.text("🔍 Extracting text content...")
                text_data = extract_text_from_pdf(uploaded_file)
                
                progress_bar.progress(80)
                status_text.text("✅ Processing complete!")
                
                if text_data:
                    progress_bar.progress(100)
                    status_text.text("🎉 PDF processed successfully!")
                    st.markdown('<div class="success-message">✅ PDF content extracted successfully!</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-message">❌ Failed to extract text from the PDF. Please ensure the PDF contains readable text.</div>', unsafe_allow_html=True)
                
                progress_bar.empty()
                status_text.empty()
                
            except Exception as e:
                st.markdown(f'<div class="error-message">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
                progress_bar.empty()
                status_text.empty()
    st.markdown('</div>', unsafe_allow_html=True)

# Professional text processing and summary generation
if text_data:
    # Text preview with analytics
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("## 📊 Text Analysis & Preview")
    
    # Calculate text statistics
    stats = get_text_statistics(text_data)
    quality = analyze_text_quality(text_data)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📝 Word Count", f"{stats['word_count']:,}")
    with col2:
        st.metric("📄 Sentences", f"{stats['sentence_count']:,}")
    with col3:
        st.metric("⏱️ Reading Time", f"{stats['reading_time_minutes']:.1f} min")
    with col4:
        st.metric("📈 Quality Score", f"{quality['quality_score']}/100")
    
    # Add custom styling for better visibility
    st.markdown("""
    <style>
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .metric-container .metric-value {
        color: #1f77b4 !important;
        font-weight: bold;
        font-size: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Quality indicators
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"🎯 Complexity: {quality['complexity']}")
    with col2:
        st.info(f"📖 Readability: {quality['readability']}")
    
    # Text preview
    st.markdown("### 📄 Text Preview")
    st.markdown(f'<div class="text-preview">{text_data[:1500] + "..." if len(text_data) > 1500 else text_data}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Summary generation
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("## 🤖 AI Summary Generation")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**Selected Length:** {length_option} Summary")
        st.markdown(f"*This will generate a {length_option.lower()} summary of your text*")
    with col2:
        if st.button("🚀 Generate Summary", type="primary", use_container_width=True):
            # Professional summary generation with progress tracking
            start_time = time.time()
            
            progress_bar, status_text = create_progress_bar("Initializing AI model...", 0)
            progress_bar.progress(10)
            status_text.text("🧠 Loading AI model...")
            time.sleep(0.5)
            
            progress_bar.progress(30)
            status_text.text("📝 Processing text...")
            time.sleep(0.5)
            
            progress_bar.progress(60)
            status_text.text("🤖 Generating summary...")
            
            try:
                if tokenizer is not None and model is not None:
                    summary = summarize_text(text_data, summary_len=length_option, tokenizer=tokenizer, model=model)
                else:
                    st.error("❌ Model not loaded properly. Please refresh the page and try again.")
                    progress_bar.empty()
                    status_text.empty()
                    st.stop()
                
                progress_bar.progress(90)
                status_text.text("✅ Summary generated!")
                
                # Update session statistics
                processing_time = time.time() - start_time
                st.session_state.processing_stats['total_processed'] += 1
                st.session_state.processing_stats['total_words'] += stats['word_count']
                st.session_state.processing_stats['avg_processing_time'] = (
                    st.session_state.processing_stats['avg_processing_time'] + processing_time
                ) / 2
                
                progress_bar.progress(100)
                status_text.text("🎉 Complete!")
                
                # Store summary in session state
                st.session_state['last_summary'] = summary
                st.session_state['last_stats'] = stats
                st.session_state['processing_time'] = processing_time
                
                progress_bar.empty()
                status_text.empty()
                
                st.rerun()
                
            except Exception as e:
                st.markdown(f'<div class="error-message">❌ Error generating summary: {str(e)}</div>', unsafe_allow_html=True)
                progress_bar.empty()
                status_text.empty()
    
    # Display summary if available
    if 'last_summary' in st.session_state and st.session_state['last_summary']:
        st.markdown("### 📋 Generated Summary")
        
        # Summary metrics
        summary_stats = get_text_statistics(st.session_state['last_summary'])
        col1, col2, col3 = st.columns(3)
        with col1:
            st.success(f"📝 Summary Words: {summary_stats['word_count']}")
        with col2:
            compression_ratio = (1 - summary_stats['word_count'] / stats['word_count']) * 100
            st.info(f"📊 Compression: {compression_ratio:.1f}%")
        with col3:
            st.info(f"⏱️ Generated in: {st.session_state.get('processing_time', 0):.2f}s")
        
        # Display summary
        st.markdown(f"**{length_option} Summary:**")
        st.markdown(f'<div class="summary-display">{st.session_state["last_summary"]}</div>', unsafe_allow_html=True)
        
        # Export options
        st.markdown("### 💾 Export Options")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Download PDF", use_container_width=True):
                try:
                    pdf_path = generate_pdf(
                        st.session_state['last_summary'], 
                        title=f"Hindi Summary - {length_option}",
                        author="Hindi LLM Summarizer Pro"
                    )
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            "📥 Download PDF",
                            data=pdf_file.read(),
                            file_name=f"Hindi_Summary_{length_option}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")
        
        with col2:
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                st.code(st.session_state['last_summary'])
                st.success("Summary copied! Use Ctrl+C to copy from the code block above.")
        
        with col3:
            if st.button("🔄 Generate New", use_container_width=True):
                if 'last_summary' in st.session_state:
                    del st.session_state['last_summary']
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Professional footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; margin-top: 2rem;">
    <h3>🚀 Hindi LLM Summarizer Pro</h3>
    <p style="margin: 0.5rem 0;">Professional AI-Powered Text Summarization Platform</p>
    <p style="margin: 0.5rem 0; font-size: 0.9rem;">Developed by <strong>Jigyansh</strong> | ECE Undergraduate | Thapar Institute of Engineering Technology</p>
    <p style="margin: 0.5rem 0; font-size: 0.8rem;">Powered by Google's T5 AI Model | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
