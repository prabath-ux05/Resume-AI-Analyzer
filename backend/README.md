# Resume AI Analyzer Backend

This is the FastAPI backend for the Resume AI Analyzer project. It provides an API for uploading PDF or DOCX resumes and extracting their text content.

## Project Structure

```
backend/
├── main.py
├── routes/
│   └── resume_routes.py
├── services/
│   └── resume_parser.py
├── uploads/              # Created automatically on upload
├── utils/
│   └── file_handler.py
├── requirements.txt
└── README.md
```

## Features
- **FastAPI Framework:** Fast, modern, and high performance.
- **File Uploads:** Securely saves uploaded files in the `uploads/` directory.
- **Text Extraction:** Uses `PyMuPDF` for PDFs and `python-docx` for DOCX.
- **Error Handling:** Gracefully handles invalid file types and extraction errors.

## Setup Instructions

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

Run the following command to start the Uvicorn server in development mode (with auto-reload):

```bash
uvicorn main:app --reload
```

The API will be available at: http://127.0.0.1:8000

## API Endpoint Usage

### POST `/upload-resume`

Uploads a resume file and extracts its text.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (the PDF or DOCX file)

**Response:**
```json
{
  "filename": "resume.pdf",
  "status": "success",
  "extracted_text": "Extracted text content from the resume..."
}
```

You can interact with the API docs (Swagger UI) at: http://127.0.0.1:8000/docs
