# backend/app/services/document_parser.py
from langchain_community.document_loaders import PyPDFLoader
from PIL import Image
import pytesseract
import os

# Point Python to your Windows Tesseract installation
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_file(file_path: str) -> str:
    """
    Checks the file extension and extracts text using either PyPDF (for PDFs) 
    or Tesseract OCR (for Images).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    ext = os.path.splitext(file_path)[1].lower()

    # Handle Standard PDFs
    if ext == '.pdf':
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        text = "\n".join([page.page_content for page in pages])
        return text

    # Handle Images (OCR)
    elif ext in ['.png', '.jpg', '.jpeg']:
        try:
            img = Image.open(file_path)
            # Use AI to read the pixels and convert them to text
            text = pytesseract.image_to_string(img)
            return text
        except Exception as e:
            raise RuntimeError(f"OCR Processing failed: {str(e)}")
    
    else:
        raise ValueError(f"Unsupported file format: {ext}")