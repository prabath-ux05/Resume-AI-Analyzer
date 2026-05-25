import re
from typing import Dict, Any, List

class LocalResumeParser:
    """
    Lightweight, fast heuristic parser to structure raw resume text
    before sending it to Gemini. Minimizes context window payload.
    """
    
    def __init__(self):
        # Common section headers in resumes
        self.sections = {
            "skills": re.compile(r'\b(skills|technical skills|core competencies)\b', re.IGNORECASE),
            "experience": re.compile(r'\b(experience|work history|employment|professional experience)\b', re.IGNORECASE),
            "education": re.compile(r'\b(education|academic background)\b', re.IGNORECASE),
            "projects": re.compile(r'\b(projects|personal projects|open source)\b', re.IGNORECASE),
            "certifications": re.compile(r'\b(certifications|licenses|awards)\b', re.IGNORECASE),
        }

    def _extract_email(self, text: str) -> str:
        match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
        return match.group(0) if match else ""

    def _extract_links(self, text: str) -> List[str]:
        return list(set(re.findall(r'(https?://[^\s]+|linkedin\.com/in/[^\s]+|github\.com/[^\s]+)', text)))

    def parse(self, raw_text: str) -> Dict[str, Any]:
        lines = raw_text.split('\n')
        
        parsed_data = {
            "contact_info": {
                "email": self._extract_email(raw_text),
                "links": self._extract_links(raw_text)
            },
            "sections": {
                "skills": "",
                "experience": "",
                "education": "",
                "projects": "",
                "certifications": "",
                "other": ""
            }
        }

        current_section = "other"
        
        for line in lines:
            line_clean = line.strip()
            if not line_clean:
                continue

            # If the line is short, it might be a header
            if len(line_clean) < 40:
                identified_section = None
                for sec_name, pattern in self.sections.items():
                    if pattern.search(line_clean):
                        identified_section = sec_name
                        break
                
                if identified_section:
                    current_section = identified_section
                    continue # Skip adding the header text itself
            
            # Append line to current section
            parsed_data["sections"][current_section] += line_clean + "\n"
        
        # Clean up whitespace
        for k in parsed_data["sections"]:
            parsed_data["sections"][k] = parsed_data["sections"][k].strip()

        return parsed_data
