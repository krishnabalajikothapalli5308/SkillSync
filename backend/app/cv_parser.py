from io import BytesIO
from pathlib import Path
from fastapi import HTTPException, UploadFile
from pypdf import PdfReader
from docx import Document

MAX_FILE_BYTES = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {".pdf", ".docx"}

async def extract_cv_text(file: UploadFile) -> str:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415, detail="Upload a PDF or DOCX file.")
    data = await file.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise HTTPException(status_code=413, detail="CV must be 5 MB or smaller.")
    try:
        if suffix == ".pdf":
            reader = PdfReader(BytesIO(data))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        else:
            doc = Document(BytesIO(data))
            text = "\n".join(p.text for p in doc.paragraphs)
            for table in doc.tables:
                for row in table.rows:
                    text += "\n" + " ".join(cell.text for cell in row.cells)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Could not read this document.") from exc
    if not text.strip():
        raise HTTPException(status_code=422, detail="No selectable text found. Use a text-based PDF or DOCX.")
    return text[:100000]
