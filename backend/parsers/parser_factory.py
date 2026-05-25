from parsers.base_parser import BaseParser
from parsers.pymupdf_parser import PyMuPDFParser
from utils.logger import logger
import os

class ParserFactory:
    """
    Factory to retrieve the appropriate parser based on file type.
    """

    @staticmethod
    def get_parser(file_path: str) -> BaseParser:
        _, ext = os.path.splitext(file_path.lower())

        if ext == ".pdf":
            return PyMuPDFParser()
        # Add support for .docx, .txt, etc. in the future
        # elif ext == ".docx":
        #     return DocxParser()
        else:
            logger.warning(f"Unsupported file extension: {ext}. Falling back to default parser or raising error.")
            raise ValueError(f"Unsupported file type: {ext}")
