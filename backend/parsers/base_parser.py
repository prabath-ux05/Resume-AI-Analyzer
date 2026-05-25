from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseParser(ABC):
    """
    Base class for all document parsers.
    Defines the interface for extracting text and metadata from files.
    """

    @abstractmethod
    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a document and return its text content and metadata.

        Args:
            file_path: The path to the file to parse.

        Returns:
            Dict containing 'text' and 'metadata'.
        """
        pass
