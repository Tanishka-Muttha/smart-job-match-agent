# Smart Job Match Agent - Local AI-Powered Job Recommendation System

A lightweight job recommendation system built using FastAPI, TF-IDF vectorization, cosine similarity, and rule-based reasoning.

The project runs completely locally without requiring paid APIs or external AI services.

---

# Features

- Resume analysis and skill extraction
- TF-IDF based job matching
- Cosine similarity ranking
- Top 5 recommended jobs with match scores
- Rule-based match explanations
- Dynamic clarifying question generation
- Interactive web interface
- FastAPI backend with REST APIs
- Fully local and free to use

---

# Web Interface

After starting the server, open:

```text
http://localhost:8000
```

The interface allows users to:
- paste resume text
- analyze skills and experience
- view recommended jobs
- see match explanations
- receive follow-up clarification questions

---

# Quick Start

## 1. Install Python

Download Python 3.9 or higher:

https://www.python.org/downloads/

Verify installation:

```bash
python --version
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Start the Server

```bash
python -m uvicorn api.index:app --reload
```

You should see:

```text
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## 5. Open the Application

Open your browser and visit:

```text
http://localhost:8000
```

---

# Example Resume Input

```text
Python developer with machine learning and SQL experience.
Skills: Python, TensorFlow, FastAPI, SQL, Docker
Interested in AI Engineer and Data Scientist roles.
```

---

# How the Project Works

## Step 1: Resume Parsing

The system extracts:
- skills
- experience
- education
- role preferences

using rule-based text parsing.

---

## Step 2: TF-IDF Vectorization

Resume text and job descriptions are converted into TF-IDF vectors using scikit-learn.

---

## Step 3: Similarity Matching

Cosine similarity is used to compare resumes with available jobs.

The system ranks the top matching jobs based on similarity score.

---

## Step 4: Match Explanations

Rule-based logic generates explanations describing why a job matches the candidate profile.

---

## Step 5: Clarifying Question

The system generates one follow-up question to better understand candidate preferences.

---

# Project Flow

```text
Resume Input
↓
Resume Parsing
↓
TF-IDF Vectorization
↓
Cosine Similarity Matching
↓
Top Job Recommendations
↓
Match Explanations
```

---

# API Endpoints

## POST /recommend

Accepts resume text and returns:
- parsed candidate profile
- ranked jobs
- match explanations
- clarifying question

Example request:

```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"resume_text":"Python developer with SQL experience"}'
```

---

## POST /refine

Optional endpoint for refining recommendations based on follow-up responses.

---

## GET /health

Checks whether the backend is running correctly.

---

## GET /docs

Interactive FastAPI Swagger documentation.

Open:

```text
http://localhost:8000/docs
```

---

# Assignment Requirements Covered

## Part 1: Embeddings and Similarity

- TF-IDF vectorization
- Cosine similarity ranking
- Top job recommendations

## Part 2: Reasoning

- Resume parsing
- Rule-based explanations
- Skill overlap analysis

## Part 3: Clarifying Question

- Dynamic question generation
- Based on resume and recommendation patterns

## Part 4: FastAPI API

- REST API endpoints
- Structured JSON responses
- Error handling

## Part 5: Deployment Ready

- Runs locally
- Compatible with Vercel deployment

---

# Troubleshooting

## "No module named fastapi"

Run:

```bash
pip install -r requirements.txt
```

---

## "Port 8000 already in use"

Run on another port:

```bash
python -m uvicorn api.index:app --reload --port 8001
```

---

## "jobs.json not found"

Ensure the following file exists:

```text
api/jobs.json
```

---

# Project Structure

```text
smart-job-match-agent-free/
│
├── api/
│   ├── index.py
│   ├── index.html
│   └── jobs.json
│
├── services/
│   ├── embeddings.py
│   ├── matcher.py
│   └── llm_agent.py
│
├── requirements.txt
├── README.md
├── QUICK_START.md
└── vercel.json
```

---

# Optional Deployment

Deploy to Vercel:

```bash
npm install -g vercel
vercel login
vercel --prod
```

---

# Technologies Used

- Python
- FastAPI
- scikit-learn
- TF-IDF Vectorization
- Cosine Similarity
- HTML/CSS/JavaScript

---

# Final Note

This project was designed to be simple, fully local, easy to run, and understandable for learning and demonstration purposes.

It avoids dependency on paid AI APIs while still demonstrating core recommendation system concepts and backend engineering.

🚀