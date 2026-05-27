# Elevora AI 🚀

### AI-Powered Resume Analysis & Career Guidance Platform

Elevora AI is a full-stack AI-driven resume intelligence platform that helps candidates analyze resumes, improve ATS performance, discover best-fit technical roles, and receive personalized AI-powered career guidance.

The platform combines:

* Generative AI
* Resume Intelligence
* ATS Analysis
* Role Matching
* AI Career Assistant
* Cloud Deployment

to simulate a modern AI recruitment ecosystem.

---

## 🌐 Live Demo

Frontend:

```bash
https://resume-ai-analyzer-two.vercel.app
```

---

# ✨ Features

## 📄 AI Resume Analysis

* Upload resumes in PDF format
* Extract structured resume intelligence
* Generate ATS scores
* Analyze resume quality and recruiter perception

---

## 🎯 AI Role Matching

* Suggests best-fit roles
* Generates role alignment scores
* Company-fit recommendations
* Industry-fit analysis

---

## 🤖 AI Career Assistant

Interactive AI chatbot for:

* Resume guidance
* Interview preparation
* Skill gap analysis
* Career roadmap suggestions
* Technical doubt clarification

---

## 📊 ATS Scoring System

Evaluates:

* Resume structure
* Technical skills
* Projects
* Experience
* ATS keywords
* Education quality

---

## 🧠 Intelligent Skill Extraction

Detects:

* Programming Languages
* Frameworks
* AI/ML Skills
* Cloud Technologies
* DevOps Tools
* Databases

---

## 📈 Improvement Roadmap

Provides:

* Missing keywords
* Skill improvement suggestions
* Recruiter keyword gaps
* Learning roadmap
* Career recommendations

---

# 🏗️ Tech Stack

## Frontend

* React.js
* Vite
* Tailwind CSS
* Axios
* Framer Motion

## Backend

* FastAPI
* Python
* Async APIs

## AI & NLP

* Groq API
* Llama 3.1 8B Instant
* Prompt Engineering
* Structured JSON Extraction
* Resume Semantic Analysis

## Database & Caching

* Supabase PostgreSQL
* Redis Cache
* SHA256 Resume Hashing

## Cloud & Deployment

* Vercel (Frontend)
* Render (Backend)
* UptimeRobot (Keep Alive Monitoring)

## Additional Tools

* Qdrant Vector DB
* PyMuPDF
* Pydantic Validation

---

# ⚙️ Architecture

```bash
User Upload Resume
        ↓
Frontend (Vercel)
        ↓
FastAPI Backend (Render)
        ↓
Resume Parsing + AI Orchestration
        ↓
Groq LLM Processing
        ↓
ATS + Role Match + AI Insights
        ↓
Redis Cache + PostgreSQL Storage
        ↓
Frontend Visualization
```

---

# 🚀 Key Engineering Highlights

## Production-Level AI Pipeline

* Structured AI orchestration
* JSON sanitization
* Schema validation
* Retry handling
* Safe fallback mechanisms

---

## Intelligent Resume Intelligence Engine

Pipeline includes:

1. Resume Parsing
2. Local Heuristic Extraction
3. AI Intelligence Generation
4. ATS Analysis
5. Role Matching
6. Career Guidance

---

## Cloud-Native Deployment

Successfully deployed:

* Frontend on Vercel
* Backend on Render
* PostgreSQL via Supabase
* Redis-based caching architecture

---

## AI Assistant System

* Resume-aware AI chatbot
* Redis conversation memory
* Streaming responses
* Career guidance assistant

---

# 🛠️ Major Challenges Solved

* Migrated Gemini → Groq architecture
* Fixed JSON parsing instability
* Solved fallback scoring issues
* Stabilized AI response formatting
* Fixed Render sleep problems
* Resolved production CORS issues
* Implemented uptime monitoring
* Improved frontend/backend API handling

---

# 📌 Future Improvements

* Voice-enabled AI assistant
* Real-time mock interviews
* PDF report generation
* Multi-language resume support
* Job portal integration
* Advanced analytics dashboard

---

# 🧪 Installation

## Clone Repository

```bash
git clone <your-repo-url>
cd elevora-ai
```

---

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

---

# 🔑 Environment Variables

## Frontend `.env`

```env
VITE_API_URL=https://your-render-backend.onrender.com
```

---

## Backend `.env`

```env
GROQ_API_KEY=your_groq_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
REDIS_URL=your_redis_url
```

---

# 📷 Screenshots

Add:

* Homepage Screenshot
* Resume Upload
* ATS Dashboard
* Role Match Results
* AI Assistant Chat
* Analytics Visualization

---

# 🎥 Demo Video

Add your project demo video link here.

Example:

```bash
https://youtu.be/your-demo-video
```

---

# 👨‍💻 Author

### Prabath D

AI/ML Engineer | Full Stack Developer | Cloud Enthusiast

* LinkedIn
* GitHub

---

# ⭐ Project Outcome

Elevora AI demonstrates:

* Full Stack Development
* AI Engineering
* Generative AI Integration
* Cloud Deployment
* Production Debugging
* Resume Intelligence Systems
* Real-Time AI Applications
* Scalable Backend Architecture

Built as a production-style AI recruitment and career guidance platform using modern software engineering and cloud-native AI practices.
