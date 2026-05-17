# ⚡ QUICK START

## What You're Getting

A completely free job recommendation system that:

- ✅ Works on any computer
- ✅ Needs no API keys
- ✅ Runs locally on your machine
- ✅ No paid services required
- ✅ Simple setup process

---

# Step 1: Download Files

Make sure you have the complete project folder:

```text
smart-job-match-agent-free
```

---

# Step 2: Install Python

If Python is not installed:

1. Go to: https://www.python.org/downloads/
2. Download Python 3.9 or higher
3. Install Python
4. Verify installation:

```bash
python --version
```

---

# Step 3: Open Terminal

Open a terminal inside the project folder.

### Windows
Right click inside the folder → Open in Terminal / PowerShell

### Mac/Linux
Right click → Open Terminal

---

# Step 4: Create Virtual Environment

Run:

```bash
python -m venv venv
```

After it finishes:

### Mac/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

You should now see:

```text
(venv)
```

at the beginning of the terminal line.

---

# Step 5: Install Dependencies

Run:

```bash
pip install -r requirements.txt
```

This installs all required Python packages.

---

# Step 6: Start the Server

Run:

```bash
python -m uvicorn api.index:app --reload
```

You should see:

```text
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Keep this terminal open while using the project.

---

# Step 7: Open the Web Application

Open your browser and go to:

```text
http://127.0.0.1:8000
```

You will see the Smart Job Match web interface.

You can:
- paste resume text
- analyze skills
- view recommended jobs
- see match explanations
- get follow-up questions

---

# Step 8: Test the API (Optional)

Open:

```text
http://127.0.0.1:8000/docs
```

This opens FastAPI Swagger documentation where you can test the API endpoints interactively.

---

# Example Resume Input

```text
Python developer with machine learning and SQL experience.
Skills: Python, TensorFlow, FastAPI, SQL, Docker
Interested in AI Engineer and Data Scientist roles.
```

---

# What the Project Does

1. Parses resume text
2. Extracts skills and role preferences
3. Converts resumes and jobs into TF-IDF vectors
4. Uses cosine similarity for matching
5. Ranks the most relevant jobs
6. Generates match explanations
7. Asks a follow-up clarification question

Everything runs locally without external APIs or paid services.

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

# Troubleshooting

## "(venv) is not recognized"

You are probably on Windows.

Use:

```bash
venv\Scripts\activate
```

---

## "No module named fastapi"

Run:

```bash
pip install -r requirements.txt
```

again.

---

## "Port 8000 already in use"

Run on another port:

```bash
python -m uvicorn api.index:app --reload --port 8001
```

---

## "jobs.json not found"

Make sure this file exists:

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

To deploy on Vercel:

```bash
npm install -g vercel
vercel login
vercel --prod
```

---

# Final Note

The project is designed to be simple to run, easy to understand, and fully local without depending on paid AI APIs.

Enjoy building and experimenting 🚀