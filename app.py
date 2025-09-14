import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import fitz  # PyMuPDF
import requests
from newspaper import Article
import tempfile
from fpdf import FPDF
import nltk
from PyPDF2 import PdfReader
import os

# Streamlit UI config
st.set_page_config(page_title="Hindi LLM Summarizer", layout="wide")

# Download punkt
nltk.download("punkt")

# Set PyTorch workaround for Windows torch.classes issue
os.environ["PYTORCH_JIT"] = "0"

# Load summarization model
@st.cache_resource
def load_model():
    model_name = "csebuetnlp/mT5_multilingual_XLSum"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

# Summarization function

def summarize_text(text, summary_len):
    input_ids = tokenizer("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True).input_ids

    if summary_len == "Short":
        max_len, min_len = 70, 30
    elif summary_len == "Medium":
        max_len, min_len = 150, 60
    else:
        max_len, min_len = 300, 120

    output = model.generate(
        input_ids,
        max_length=max_len,
        min_length=min_len,
        num_beams=4,
        length_penalty=2.0,
        early_stopping=True
    )
    return tokenizer.decode(output[0], skip_special_tokens=True)

# PDF text extraction (typed only)
def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception:
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

# PDF generator for summary
def generate_pdf(summary):
    pdf = FPDF()
    pdf.add_page()
    font_path = os.path.join(os.path.dirname(__file__), "fonts", "NotoSansDevanagari-Regular.ttf")
    if not os.path.exists(font_path):
        raise FileNotFoundError("fonts/NotoSansDevanagari-Regular.ttf not found in the project directory.")
    pdf.add_font("NotoSans", "", font_path, uni=True)
    pdf.set_font("NotoSans", size=14)
    for line in summary.split("\n"):
        pdf.multi_cell(0, 10, txt=line)
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp_file.name)
    return tmp_file.name

# UI layout
st.title("Hindi LLM Summarizer")
st.markdown("""
Choose input type and get a summary of your content in Hindi.

**Summary Length Options:**
- **Short**: ~15–25 words
- **Medium**: ~30–50 words
- **Long**: ~80+ words  
(Maximum input allowed: 1200 words for manual input)
""")

input_type = st.radio("Choose input type:", ["Manual Hindi Text", "Enter Article URL", "Upload PDF"])

length_option = st.selectbox("Select summary length", ["Short", "Medium", "Long"])

text_data = ""

if input_type == "Manual Hindi Text":
    st.subheader("Enter Hindi Text")
    manual_input = st.text_area("Type or paste your Hindi text here (max 1200 words):", height=250, key="manual_text_input")
    word_count = len(manual_input.split())
    if word_count > 1200:
        st.warning("Input exceeds 1200 words. It will be truncated.")
        manual_input = " ".join(manual_input.split()[:1200])
    text_data = manual_input

elif input_type == "Enter Article URL":
    url = st.text_input("Paste the article URL:")
    if url:
        with st.spinner("Extracting content from URL..."):
            text_data = extract_text_from_url(url)
        if text_data:
            st.success("Text extracted successfully.")
        else:
            st.error("Failed to extract content from the URL.")

elif input_type == "Upload PDF":
    uploaded_file = st.file_uploader("Upload a typed Hindi PDF (max 20 pages)", type="pdf")
    if uploaded_file:
        with st.spinner("Extracting text from PDF..."):
            text_data = extract_text_from_pdf(uploaded_file)
        if text_data:
            st.success("Text extracted successfully from PDF.")
        else:
            st.error("Failed to extract text from the uploaded PDF.")

if text_data:
    st.subheader("Extracted Text Preview:")
    st.text_area("Preview", value=text_data[:1500], height=200, disabled=True)

    if st.button("Generate Hindi Summary"):
        with st.spinner("Summarizing..."):
            summary = summarize_text(text_data, summary_len=length_option)
        st.subheader("Hindi Summary:")
        st.write(summary)

        pdf_path = generate_pdf(summary)
        with open(pdf_path, "rb") as pdf_file:
            st.download_button("Download Summary as PDF", data=pdf_file.read(),
                               file_name="Hindi_Summary.pdf", mime="application/pdf")

# Footer
st.markdown("""
---
**Created by Jigyansh**, ECE undergraduate, Thapar Institute of Engineering Technology
""")
