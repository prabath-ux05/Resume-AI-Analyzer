import fitz  # PyMuPDF
import docx

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file using PyMuPDF.
    """
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        raise Exception(f"Failed to read PDF: {str(e)}")

def extract_text_from_docx(file_path: str) -> str:
    """
    Extracts text from a DOCX file using python-docx.
    """
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        raise Exception(f"Failed to read DOCX: {str(e)}")

def parse_resume(file_path: str, filename: str) -> str:
    """
    Detects file extension and routes to the appropriate extraction function.
    """
    ext = filename.split(".")[-1].lower()
    
    if ext == "pdf":
        return extract_text_from_pdf(file_path)
    elif ext == "docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or DOCX.")
