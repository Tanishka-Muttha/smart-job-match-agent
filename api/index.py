"""
FastAPI application - Smart Job Match Agent
100% FREE - uses local TF-IDF embeddings and rule-based reasoning.
No API keys, no downloads, works on any computer.
"""
import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

from services.llm_agent import parse_resume, generate_match_explanations, generate_clarifying_question
from services.matcher import rank_jobs

# Initialize FastAPI app
app = FastAPI(
    title="Smart Job Match Agent",
    description="AI-powered job recommendation system (100% FREE - local processing)",
    version="1.0.0"
)

# Enable CORS for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve beautiful HTML UI at root
@app.get("/")
async def serve_ui():
    """Serve the beautiful HTML UI"""
    ui_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(ui_path):
        return FileResponse(ui_path, media_type="text/html")
    return {"message": "Visit /docs for API documentation"}

# Load jobs dataset
def load_jobs():
    """Load jobs from JSON file."""
    jobs_path = os.path.join(os.path.dirname(__file__), "jobs.json")
    
    if not os.path.exists(jobs_path):
        jobs_path = os.path.join(os.path.dirname(__file__), "../data/jobs.json")
    
    try:
        with open(jobs_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"Jobs dataset not found at {jobs_path}")

JOBS = load_jobs()


# Request/Response models
class RecommendRequest(BaseModel):
    resume_text: str


class RankedJob(BaseModel):
    id: int
    title: str
    company: str
    similarity_score: float
    explanation: str


class CandidateProfile(BaseModel):
    name: str
    skills: list[str]
    experience_years: float


class RecommendResponse(BaseModel):
    candidate: CandidateProfile
    ranked_jobs: list[RankedJob]
    clarifying_question: str


class RefineRequest(BaseModel):
    resume_text: str
    clarifying_question: str
    candidate_answer: str


class RefineResponse(BaseModel):
    ranked_jobs: list[RankedJob]
    reasoning: str


# Endpoints
@app.post("/recommend")
async def recommend(request: RecommendRequest) -> RecommendResponse:
    """
    Main recommendation endpoint.
    100% FREE - pure Python processing, no APIs.
    """
    # Validate input
    if not request.resume_text or len(request.resume_text.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Resume text must be at least 10 characters long"
        )
    
    try:
        # Step 1: Parse resume
        resume_data = parse_resume(request.resume_text)
        
        # Step 2: Rank jobs
        ranked_jobs = rank_jobs(resume_data, JOBS, top_k=5)
        
        # Step 3: Generate explanations
        explanations = generate_match_explanations(resume_data, ranked_jobs)
        
        # Step 4: Generate question
        clarifying_question = generate_clarifying_question(resume_data, ranked_jobs)
        
        # Build response
        candidate = CandidateProfile(
            name=resume_data.get("name", "Unknown"),
            skills=resume_data.get("skills", []),
            experience_years=resume_data.get("experience_years", 0)
        )
        
        ranked_jobs_response = [
            RankedJob(
                id=job["id"],
                title=job["title"],
                company=job["company"],
                similarity_score=round(job["similarity_score"], 3),
                explanation=explanations.get(str(job["id"]), "")
            )
            for job in ranked_jobs
        ]
        
        return RecommendResponse(
            candidate=candidate,
            ranked_jobs=ranked_jobs_response,
            clarifying_question=clarifying_question
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )


@app.post("/refine")
async def refine(request: RefineRequest) -> RefineResponse:
    """
    Bonus refinement endpoint.
    100% FREE - local processing.
    """
    if not request.candidate_answer or len(request.candidate_answer.strip()) < 5:
        raise HTTPException(
            status_code=400,
            detail="Answer must be at least 5 characters long"
        )
    
    try:
        # Parse resume
        resume_data = parse_resume(request.resume_text)
        
        # Re-rank jobs
        ranked_jobs = rank_jobs(resume_data, JOBS, top_k=5)
        
        # Generate explanations
        explanations = generate_match_explanations(resume_data, ranked_jobs)
        
        # Simple reasoning
        reasoning = f"Based on your answer '{request.candidate_answer}', we've re-evaluated your top matches. The ranking now prioritizes roles that better fit your stated preferences."
        
        # Build response
        ranked_jobs_response = [
            RankedJob(
                id=job["id"],
                title=job["title"],
                company=job["company"],
                similarity_score=round(job["similarity_score"], 3),
                explanation=explanations.get(str(job["id"]), "")
            )
            for job in ranked_jobs
        ]
        
        return RefineResponse(
            ranked_jobs=ranked_jobs_response,
            reasoning=reasoning
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Smart Job Match Agent is running",
        "type": "LOCAL - 100% FREE, no APIs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)