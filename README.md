# 🚀 AscendAI - Resume Intelligence & Career Guidance Platform

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-blue)
![Redis](https://img.shields.io/badge/Redis-Cache-red)
![Qdrant](https://img.shields.io/badge/Qdrant-VectorDB-purple)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![Vercel](https://img.shields.io/badge/Vercel-Frontend-black)
![Render](https://img.shields.io/badge/Render-Backend-46E3B7)

---

## 📌 Overview

AscendAI is a full-stack AI-powered Resume Intelligence Platform designed to analyze resumes, generate ATS scores, perform semantic role matching, and provide personalized career guidance through an AI assistant.

The platform transforms unstructured resume documents into structured intelligence using modern AI orchestration techniques, caching systems, vector retrieval infrastructure, and cloud-native deployment practices.

Unlike traditional resume scanners that rely solely on keyword matching, AscendAI combines semantic analysis, role suitability assessment, recruiter-style feedback, and conversational career guidance to help candidates improve employability and interview readiness.

---

## ✨ Core Features

### 📄 Resume Intelligence

- ATS Score Generation
- Resume Quality Assessment
- Recruiter-style Feedback
- Skill Extraction
- Resume Improvement Suggestions

### 🎯 AI Role Matching

- Resume-to-Role Alignment
- Career Suitability Analysis
- Missing Skill Detection
- Role Recommendation Engine

### 💬 Career Guidance Assistant

- Resume-aware AI Chat
- Career Roadmaps
- Interview Preparation
- Skill Development Suggestions
- Personalized Career Guidance

### ⚡ Platform Engineering

- Redis-based Caching
- AI Response Stabilization
- Retry & Fallback Mechanisms
- Resume Hashing
- Cloud-native Deployment
- Semantic Retrieval Infrastructure

---

## 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │      React UI       │
                         │ Vite + Tailwind CSS │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    FastAPI API      │
                         │ Application Layer   │
                         └──────────┬──────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼

 ┌───────────────┐        ┌────────────────┐       ┌─────────────────┐
 │ Redis Cache   │        │ AI Orchestrator│       │ PostgreSQL DB   │
 │ Response Cache│        │ Groq + Llama   │       │ Supabase        │
 └───────────────┘        └────────────────┘       └─────────────────┘
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ Qdrant VectorDB │
                          │ Semantic Search │
                          └─────────────────┘
```

---

<details>
<summary><strong>⚙️ Tech Stack</strong></summary>

### 🎨 Frontend

- React.js
- Vite
- Tailwind CSS
- Framer Motion
- Axios
- React Router
- Recharts

### 🧩 Backend

- FastAPI
- Python
- Async APIs
- Pydantic Validation
- SQLAlchemy
- PyMuPDF
- python-docx

### 🤖 AI & NLP

- Groq API
- Llama 3.1 8B Instant
- Prompt Engineering
- Structured JSON Extraction
- Resume Semantic Analysis

### 🗄️ Database & Infrastructure

- Supabase PostgreSQL
- Redis Cache
- Qdrant Vector Database
- SHA256 Resume Hashing
- Docker Compose

### ☁️ Cloud & Deployment

- Vercel
- Render
- UptimeRobot

</details>

---

## 🔄 Technical Workflow

```text
Resume Upload
      │
      ▼
Resume Parsing
      │
      ▼
Resume Hashing
      │
      ▼
Redis Cache Lookup
      │
      ▼
AI Resume Analysis
      │
      ├── ATS Scoring
      ├── Skill Extraction
      ├── Recruiter Feedback
      ├── Semantic Analysis
      └── Role Matching
      │
      ▼
Database Persistence
      │
      ▼
Frontend Visualization
```

---

## 🖼️ Platform Preview

### Dashboard & Resume Intelligence

<p align="center">
  <img src="docs/dashboard.png" width="48%" />
  <img src="docs/resume-analysis.png" width="48%" />
</p>

### Role Matching & Career Guidance

<p align="center">
  <img src="docs/role-matching.png" width="48%" />
  <img src="docs/career-guidance.png" width="48%" />
</p>

---

<details>
<summary><strong>📁 Project Structure</strong></summary>

```text
Resume-AI-Platform/
│
├── backend/
│   ├── api/
│   ├── database/
│   ├── models/
│   ├── parsers/
│   ├── prompts/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── uploads/
│   ├── utils/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── routes/
│   │   ├── services/
│   │   └── context/
│
├── docs/
│   ├── dashboard.png
│   ├── resume-analysis.png
│   ├── role-matching.png
│   └── career-assistant.png
│
├── docker-compose.yml
├── vercel.json
└── README.md
```

</details>

---

## 🔌 API Architecture

```text
Client
  │
  ▼
FastAPI Router
  │
  ▼
Service Layer
  │
  ▼
AI Orchestrator
  │
  ▼
Redis / PostgreSQL / Qdrant
```

### Core Endpoints

```http
POST   /api/v1/analyze-resume
POST   /api/v1/job-match
POST   /api/v1/job-match/auto

POST   /api/v1/chat/message
POST   /api/v1/chat/interview

GET    /api/v1/history
GET    /api/v1/chat/history
```

---

## 📊 ATS Analysis Pipeline

The ATS engine evaluates resumes through a structured processing workflow.

### Pipeline Stages

1. Resume Parsing
2. Data Normalization
3. Skill Extraction
4. Keyword Relevance Analysis
5. Experience Evaluation
6. ATS Score Generation
7. Recruiter Feedback Generation

### Objectives

- Identify missing keywords
- Evaluate role alignment
- Assess resume completeness
- Generate actionable recommendations

---

## 🧠 Resume Semantic Intelligence

Traditional ATS systems focus primarily on keyword matching.

AscendAI introduces semantic intelligence by evaluating:

- Technical Skills
- Project Relevance
- Career Trajectory
- Domain Alignment
- Experience Context

This enables deeper role matching beyond exact keyword occurrences.

---

## ⚡ Redis Caching Layer

Redis is used to reduce repeated AI processing and improve response performance.

### Cached Components

- Resume Analysis Results
- ATS Scores
- Role Matching Outputs
- AI Guidance Responses

### Benefits

- Reduced API Calls
- Lower Latency
- Faster User Experience
- Increased System Throughput

---

## 🧬 Vector Database Layer

Qdrant serves as the semantic retrieval infrastructure.

```text
Resume Content
      │
      ▼
Embedding Generation
      │
      ▼
Vector Storage
      │
      ▼
Similarity Search
      │
      ▼
Role Matching
```

### Benefits

- Semantic Search
- Similarity Retrieval
- Future RAG Integration
- Enhanced Role Recommendations

---

## ☁️ Deployment Architecture

```text
                    Internet
                        │
                        ▼

               ┌────────────────┐
               │     Vercel     │
               │ Frontend Layer │
               └───────┬────────┘
                       │
                       ▼

               ┌────────────────┐
               │     Render     │
               │ FastAPI Backend│
               └───────┬────────┘
                       │
      ┌────────────────┼─────────────────┐
      ▼                ▼                 ▼

 PostgreSQL        Redis Cache       Qdrant DB
  Supabase
```

---

## 🚀 Local Development Setup

### Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn main:app --reload
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

### Docker

```bash
docker-compose up --build
```

---

## 🔐 Environment Variables

### Backend

```env
GROQ_API_KEY=

DATABASE_URL=

REDIS_URL=

QDRANT_URL=
QDRANT_API_KEY=
```

### Frontend

```env
VITE_API_URL=
```

---

## 🛠️ Engineering Highlights

- Async FastAPI Architecture
- Service-Oriented Backend Design
- AI Response Stabilization
- Structured JSON Validation
- Retry & Fallback Mechanisms
- Redis-based Caching
- Resume Hashing for Deduplication
- Semantic Role Matching
- Vector Database Integration
- Cloud-native Deployment
- Modular API Design

---

## 🔮 Future Enhancements

### Platform

- Multi-Resume Comparison
- Resume Version Tracking
- Recruiter Dashboard
- Candidate Benchmarking

### AI

- RAG-based Career Guidance
- Multi-Model Inference
- Interview Simulation Engine
- Adaptive Learning Paths

### Infrastructure

- GitHub Actions CI/CD
- Prometheus Monitoring
- Grafana Dashboards
- OpenTelemetry Tracing
- Kubernetes Deployment
- Distributed Caching

---

## 📄 License

This project is intended for educational, research, and portfolio purposes.

---

## 👨‍💻 Author

**Prabath D**


