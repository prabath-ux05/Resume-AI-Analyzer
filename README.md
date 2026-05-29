# AscendAI

### Resume Intelligence & Career Guidance Platform

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-blue)
![Redis](https://img.shields.io/badge/Redis-Cache-red)
![Qdrant](https://img.shields.io/badge/Qdrant-VectorDB-purple)
![Vercel](https://img.shields.io/badge/Vercel-Frontend-black)
![Render](https://img.shields.io/badge/Render-Backend-46E3B7)

---

## Overview

AscendAI is a production-oriented resume intelligence platform designed to provide structured resume analysis, ATS diagnostics, semantic role matching, recruiter-style feedback, and AI-driven career guidance.

The platform combines modern AI orchestration techniques, vector retrieval systems, structured LLM pipelines, caching strategies, and cloud-native deployment practices to deliver reliable and scalable resume intelligence workflows.

Rather than functioning as a simple resume scanner, AscendAI focuses on transforming unstructured resume documents into actionable career insights through semantic analysis, intelligent role matching, and conversational guidance.

---

## Core Capabilities

### Resume Intelligence

* ATS score generation
* Resume quality assessment
* Skill extraction
* Experience evaluation
* Recruiter-style diagnostics
* Resume improvement recommendations

### AI Career Guidance

* Resume-aware AI assistant
* Career pathway recommendations
* Skill gap identification
* Interview preparation guidance
* Learning roadmap generation

### Semantic Role Matching

* Embedding-based role similarity
* Resume-to-role alignment scoring
* Career suitability analysis
* Role recommendation engine

### Infrastructure Features

* Redis-based response caching
* Vector retrieval pipeline
* AI response stabilization
* Structured JSON enforcement
* Retry and fallback mechanisms
* Cloud-native deployment architecture

---

# System Architecture

```text
                        ┌──────────────────┐
                        │    React UI      │
                        │  Vite + Tailwind │
                        └─────────┬────────┘
                                  │
                                  ▼
                        ┌──────────────────┐
                        │ FastAPI Backend  │
                        │ API Gateway      │
                        └───────┬──────────┘
                                │
           ┌────────────────────┼────────────────────┐
           ▼                    ▼                    ▼

 ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
 │ Redis Cache    │  │ AI Orchestrator│  │ PostgreSQL     │
 │ Response Layer │  │ Llama 3.1      │  │ Resume Storage │
 └────────────────┘  └────────────────┘  └────────────────┘
                                │
                                ▼

                     ┌─────────────────────┐
                     │ Qdrant Vector Store │
                     │ Semantic Retrieval  │
                     └─────────────────────┘
```

---

# Technical Workflow

```text
Resume Upload
      │
      ▼
Resume Parsing
      │
      ▼
Data Normalization
      │
      ▼
ATS Analysis Pipeline
      │
      ▼
Semantic Feature Extraction
      │
      ▼
Vector Embedding Generation
      │
      ▼
Role Matching Engine
      │
      ▼
AI Career Guidance Layer
      │
      ▼
Structured Response Generation
      │
      ▼
Frontend Visualization
```

---

# ATS Analysis Pipeline

The ATS pipeline converts uploaded resumes into structured candidate profiles through a multi-stage processing workflow.

### Pipeline Stages

1. Resume ingestion
2. Text extraction
3. Data normalization
4. Skill detection
5. Experience evaluation
6. ATS scoring
7. Feedback generation

Key objectives:

* Detect missing keywords
* Evaluate role alignment
* Assess resume completeness
* Generate recruiter-style recommendations

---

# Resume Semantic Analysis

Traditional ATS systems primarily rely on keyword matching.

AscendAI introduces semantic analysis capabilities by evaluating:

* Technical skills
* Project relevance
* Experience context
* Career trajectory
* Domain alignment

This enables deeper role matching beyond exact keyword occurrences.

---

# Vector Retrieval Pipeline

Qdrant is used as the semantic retrieval layer.

### Workflow

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

Benefits:

* Semantic search
* Similar candidate profiling
* Improved role recommendations
* Reduced keyword dependency

---

# Redis Caching Strategy

Redis is used to minimize repeated AI processing.

### Cached Components

* Resume analysis results
* ATS scores
* Role matching outputs
* AI guidance responses

### Benefits

* Reduced latency
* Lower API costs
* Faster user experience
* Increased system throughput

---

# AI Orchestration Layer

The orchestration service manages all LLM interactions.

### Responsibilities

* Prompt construction
* Schema enforcement
* Retry handling
* Response validation
* JSON sanitization
* Fallback execution

### Reliability Features

* Structured output validation
* Parsing recovery logic
* Hallucination reduction techniques
* Error containment

---

# API Architecture

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
Cache / Database / Vector Store
```

### Design Principles

* Separation of concerns
* Async request handling
* Schema-driven validation
* Service-oriented architecture

---

# Deployment Architecture

```text
                     Internet
                         │
                         ▼

                 ┌─────────────┐
                 │   Vercel    │
                 │ Frontend UI │
                 └──────┬──────┘
                        │
                        ▼

                 ┌─────────────┐
                 │   Render    │
                 │ FastAPI API │
                 └──────┬──────┘
                        │
      ┌─────────────────┼─────────────────┐
      ▼                 ▼                 ▼

 PostgreSQL        Redis Cache      Qdrant DB
  Supabase

```

### Monitoring

* UptimeRobot health checks
* Endpoint monitoring
* Availability tracking

---

# Engineering Highlights

### Backend Engineering

* Async FastAPI architecture
* Typed request validation
* Service-layer abstraction
* Error isolation

### AI Engineering

* Structured JSON generation
* Prompt orchestration
* Semantic analysis pipeline
* Response stabilization

### Infrastructure Engineering

* Redis caching
* Vector retrieval systems
* Cloud-native deployment
* Health monitoring

### Reliability Engineering

* Retry mechanisms
* Fallback workflows
* Response validation
* Failure recovery

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/ascendai.git

cd ascendai
```

## Frontend

```bash
cd frontend

npm install

npm run dev
```

## Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn main:app --reload
```

---

# Environment Variables

## Backend

```env
GROQ_API_KEY=

SUPABASE_URL=
SUPABASE_KEY=

REDIS_URL=

QDRANT_URL=
QDRANT_API_KEY=
```

## Frontend

```env
VITE_API_BASE_URL=
```

---

# Screenshots

## Dashboard

```text
docs/screenshots/dashboard.png
```

## Resume Analysis

```text
docs/screenshots/resume-analysis.png
```

## AI Career Guidance

```text
docs/screenshots/career-guidance.png
```

## Role Matching

```text
docs/screenshots/role-matching.png
```

---

# Demo

Frontend

```text
https://your-vercel-url.vercel.app
```

Backend

```text
https://your-render-url.onrender.com
```

API Docs

```text
https://your-render-url.onrender.com/docs
```

---

# Future Enhancements

### Platform

* Multi-resume comparison
* Candidate benchmarking
* Recruiter analytics dashboard
* Resume version tracking

### AI

* RAG-based career guidance
* Multi-model inference support
* Interview simulation engine
* Adaptive learning pathways

### Infrastructure

* Docker deployment
* Kubernetes orchestration
* CI/CD pipelines
* Observability stack
* Distributed caching

---

# Documentation

Additional technical documentation is available under:

```text
docs/
├── architecture/
├── workflows/
├── api/
└── deployment/
```

---

# License

MIT License
