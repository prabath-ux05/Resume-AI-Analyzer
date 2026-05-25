import re

def clean_resume_text(text: str) -> str:
    """
    Cleans raw extracted resume text to make it NLP-ready.
    Preserves structural integrity, headings, and readability.
    """
    if not text:
        return text

    # 1. Remove unicode invisible characters (e.g., zero-width spaces, BOM)
    text = re.sub(r'[\u200b\u200c\u200d\u200e\u200f\ufeff]', '', text)

    # 2. Remove trailing and leading spaces from each line
    lines = [line.strip() for line in text.split('\n')]
    
    # 3. Remove excessive empty lines (keep maximum 2 consecutive newlines for paragraph/section spacing)
    text = '\n'.join(lines)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # 4. Replace multiple spaces and tabs with a single space to remove duplicate spaces
    text = re.sub(r'[ \t]{2,}', ' ', text)
    
    # 5. Final strip to remove leading/trailing whitespace from the entire document
    return text.strip()
