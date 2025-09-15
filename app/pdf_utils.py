"""
PDF Processing Utilities
Handles PDF text extraction with OCR fallback
"""

import asyncio
import os
import tempfile
from typing import Optional
import fitz  # PyMuPDF
import PyPDF2
from io import BytesIO

class PDFProcessor:
    def __init__(self):
        self.max_pages = 15  # Limit to 15 pages as per requirements
    
    async def extract_text(self, pdf_path: str) -> str:
        """Extract text from PDF with multiple fallback methods"""
        try:
            # Method 1: Try PyMuPDF (fitz) first
            text = await self._extract_with_pymupdf(pdf_path)
            if text and len(text.strip()) > 50:
                return text
            
            # Method 2: Fallback to PyPDF2
            text = await self._extract_with_pypdf2(pdf_path)
            if text and len(text.strip()) > 50:
                return text
            
            # Method 3: OCR fallback (if needed)
            # For now, return what we have
            return text or "No readable text found in PDF"
            
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    async def _extract_with_pymupdf(self, pdf_path: str) -> str:
        """Extract text using PyMuPDF"""
        try:
            doc = fitz.open(pdf_path)
            text_parts = []
            
            # Limit to max_pages
            page_count = min(len(doc), self.max_pages)
            
            for page_num in range(page_count):
                page = doc.load_page(page_num)
                text = page.get_text()
                if text.strip():
                    text_parts.append(text)
            
            doc.close()
            return "\n".join(text_parts)
            
        except Exception as e:
            print(f"PyMuPDF extraction failed: {e}")
            return ""
    
    async def _extract_with_pypdf2(self, pdf_path: str) -> str:
        """Extract text using PyPDF2 as fallback"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_parts = []
                
                # Limit to max_pages
                page_count = min(len(pdf_reader.pages), self.max_pages)
                
                for page_num in range(page_count):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    if text.strip():
                        text_parts.append(text)
                
                return "\n".join(text_parts)
                
        except Exception as e:
            print(f"PyPDF2 extraction failed: {e}")
            return ""
    
    async def get_pdf_info(self, pdf_path: str) -> dict:
        """Get PDF metadata and page count"""
        try:
            doc = fitz.open(pdf_path)
            page_count = len(doc)
            
            # Get metadata
            metadata = doc.metadata
            
            doc.close()
            
            return {
                "page_count": page_count,
                "title": metadata.get("title", "Untitled"),
                "author": metadata.get("author", "Unknown"),
                "subject": metadata.get("subject", ""),
                "creator": metadata.get("creator", ""),
                "producer": metadata.get("producer", ""),
                "creation_date": metadata.get("creationDate", ""),
                "modification_date": metadata.get("modDate", "")
            }
            
        except Exception as e:
            return {
                "page_count": 0,
                "title": "Unknown",
                "author": "Unknown",
                "error": str(e)
            }
    
    async def validate_pdf(self, pdf_path: str) -> tuple[bool, str]:
        """Validate PDF file and check if it meets requirements"""
        try:
            info = await self.get_pdf_info(pdf_path)
            
            if info["page_count"] == 0:
                return False, "PDF appears to be empty or corrupted"
            
            if info["page_count"] > self.max_pages:
                return False, f"PDF has {info['page_count']} pages. Maximum allowed is {self.max_pages} pages."
            
            return True, "PDF is valid"
            
        except Exception as e:
            return False, f"Error validating PDF: {str(e)}"

