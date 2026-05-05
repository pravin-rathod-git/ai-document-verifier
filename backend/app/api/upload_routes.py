# backend/app/api/upload_routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
from pathlib import Path

# Import our services
from app.services.document_parser import extract_text_from_file
from app.services.extraction_service import extract_data_from_text
from app.services.rag_service import add_to_vector_store

router = APIRouter()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # 1. Validate file extension (Now accepting images!)
    allowed_extensions = {".pdf", ".png", ".jpg", ".jpeg"}
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Currently, only {allowed_extensions} files are supported.")

    save_path = UPLOAD_DIR / file.filename

    # 2. Save the file to disk
    try:
        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    finally:
        file.file.close()

# 3. Extract text (Will automatically route to PDF or OCR based on file type)
    try:
        raw_text = extract_text_from_file(str(save_path))
    except Exception as e:
        # This catches actual crashes (like Tesseract not being found)
        raise HTTPException(status_code=500, detail=f"Failed to parse text: {str(e)}")

    # Security check: Placed OUTSIDE the try block so it triggers a clean 400 error
    if not raw_text or not raw_text.strip():
        raise HTTPException(
            status_code=400, 
            detail="The AI successfully scanned the image, but couldn't read any text. Please ensure the image is clear, has good contrast, and contains text."
        )
    # ... (Keep the rest of your code for JSON extraction and Pinecone exactly the same)
    # 4. Use Mistral AI to extract structured JSON data
    try:
        extracted_json = extract_data_from_text(raw_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Extraction failed: {str(e)}")

    # 5. Save the text to Pinecone Vector Database!
    try:
        chunks_saved = add_to_vector_store(raw_text, file.filename)
    except Exception as e:
        # If this fails, we want to see the EXACT error in the terminal
        print(f"\n❌ PINECONE ERROR: {str(e)}\n")
        chunks_saved = 0

    # 6. Return the final data
    return {
        "status": "success",
        "filename": file.filename,
        "text_length": len(raw_text),
        "chunks_indexed": chunks_saved,
        "extracted_data": extracted_json
    }