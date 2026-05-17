# Smart Job Match Agent – Lightweight NLP-Based Job Recommendation System

A lightweight job recommendation system built using FastAPI, TF-IDF vectorization, cosine similarity, and rule-based reasoning.

The project runs locally without requiring paid APIs or external AI services.

---

## Features

- Resume analysis and skill extraction
- TF-IDF based semantic matching
- Cosine similarity ranking
- Top 5 recommended jobs with match scores
- Match explanations
- Clarifying question generation
- Interactive web interface
- FastAPI REST APIs
- Deployable on Vercel

---

## Tech Stack

- Python
- FastAPI
- Scikit-Learn
- TF-IDF Vectorization
- Cosine Similarity
- HTML/CSS/JavaScript
- Vercel

---

## Quick Start

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Mac/Linux

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Server

```bash
python -m uvicorn api.index:app --reload
```

---

## Open Application

Frontend UI:

```bash
http://localhost:8000
```

Swagger API Docs:

```bash
http://localhost:8000/docs
```

---

## Example Resume Input

```text
Python developer with machine learning and SQL experience.
Skills: Python, FastAPI, SQL, Docker, TensorFlow
Interested in AI Engineer and Data Scientist roles.
```

---

## How It Works

1. Resume text is parsed using rule-based logic
2. Resume and jobs are converted into TF-IDF vectors
3. Cosine similarity compares resume with jobs
4. Top matching jobs are ranked
5. Match explanations and clarifying question are generated

---

## API Endpoints

### POST `/recommend`

Returns:
- parsed profile
- ranked jobs
- match scores
- explanations
- clarifying question

### GET `/health`

Checks backend status.

### GET `/docs`

Interactive FastAPI Swagger documentation.

---

## Project Structure

```text
smart-job-match-agent/
│
├── api/
├── services/
├── README.md
├── WRITEUP.md
├── requirements.txt
└── vercel.json
```

---

## Important Note

Initially, transformer embeddings and external LLM APIs (Gemini/HuggingFace/OpenAI) were explored. However, due to free-tier API limits and deployment size constraints on Vercel, the final version uses a lightweight TF-IDF based architecture for stable deployment and fully free usage.

The project still demonstrates semantic matching, recommendation ranking, backend engineering, deployment, and modular system design.

🚀