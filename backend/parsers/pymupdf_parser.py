import fitz  # PyMuPDF
from parsers.base_parser import BaseParser
from typing import Dict, Any
from utils.logger import logger

class PyMuPDFParser(BaseParser):
    """
    Parser for PDF files using PyMuPDF (fitz).
    Provides fast and reliable text extraction, handling complex layouts.
    """

    def parse(self, file_path: str) -> Dict[str, Any]:
        logger.info(f"Parsing PDF file with PyMuPDF: {file_path}")
        try:
            doc = fitz.open(file_path)
            full_text = ""
            metadata = {
                "page_count": len(doc),
                "format": "PDF",
                "producer": doc.metadata.get("producer", ""),
                "creator": doc.metadata.get("creator", "")
            }

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                # extract_text automatically handles some layout structures
                text = page.get_text("text")
                full_text += text + "\n"

            return {
                "text": full_text.strip(),
                "metadata": metadata
            }
        except Exception as e:
            logger.error(f"Error parsing PDF with PyMuPDF: {e}")
            raise
