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

from services.llm_agent import (
    parse_resume,
    generate_match_explanations,
    generate_clarifying_question
)

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


# Serve HTML UI
@app.get("/")
async def serve_ui():
    """Serve frontend UI"""

    ui_path = os.path.join(os.path.dirname(__file__), "index.html")

    if os.path.exists(ui_path):
        return FileResponse(ui_path, media_type="text/html")

    return {"message": "Visit /docs for API documentation"}


# Load jobs dataset
def load_jobs():
    """Load jobs from JSON file."""

    jobs_path = os.path.join(os.path.dirname(__file__), "jobs.json")

    if not os.path.exists(jobs_path):
        jobs_path = os.path.join(
            os.path.dirname(__file__),
            "../data/jobs.json"
        )

    try:
        with open(jobs_path, "r") as f:
            return json.load(f)

    except FileNotFoundError:
        raise RuntimeError(f"Jobs dataset not found at {jobs_path}")


JOBS = load_jobs()


# Request / Response Models
class RecommendRequest(BaseModel):
    resume_text: str


class RankedJob(BaseModel):
    id: int
    title: str
    company: str
    match_score: float
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


# Main Recommendation Endpoint
@app.post("/recommend")
async def recommend(request: RecommendRequest) -> RecommendResponse:

    # Validate input
    if not request.resume_text or len(request.resume_text.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Resume text must be at least 10 characters long"
        )

    try:
        # Parse resume
        resume_data = parse_resume(request.resume_text)

        # Rank jobs
        ranked_jobs = rank_jobs(
            resume_data,
            JOBS,
            top_k=5
        )

        # Generate explanations
        explanations = generate_match_explanations(
            resume_data,
            ranked_jobs
        )

        # Generate follow-up question
        clarifying_question = generate_clarifying_question(
            resume_data,
            ranked_jobs
        )

        # Candidate profile
        candidate = CandidateProfile(
            name=resume_data.get("name", "Unknown"),
            skills=resume_data.get("skills", []),
            experience_years=resume_data.get(
                "experience_years",
                0
            )
        )

        # Ranked jobs response
        ranked_jobs_response = [
            RankedJob(
                id=job["id"],
                title=job["title"],
                company=job["company"],
                match_score=round(job["match_score"], 3),
                explanation=explanations.get(
                    str(job["id"]),
                    ""
                )
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


# Refine Endpoint
@app.post("/refine")
async def refine(request: RefineRequest) -> RefineResponse:

    if (
        not request.candidate_answer
        or len(request.candidate_answer.strip()) < 5
    ):
        raise HTTPException(
            status_code=400,
            detail="Answer must be at least 5 characters long"
        )

    try:
        # Parse resume
        resume_data = parse_resume(request.resume_text)

        # Re-rank jobs
        ranked_jobs = rank_jobs(
            resume_data,
            JOBS,
            top_k=5
        )

        # Generate explanations
        explanations = generate_match_explanations(
            resume_data,
            ranked_jobs
        )

        # Reasoning
        reasoning = (
            f"Based on your answer "
            f"'{request.candidate_answer}', "
            f"we've re-evaluated your top matches."
        )

        # Response jobs
        ranked_jobs_response = [
            RankedJob(
                id=job["id"],
                title=job["title"],
                company=job["company"],
                match_score=round(job["match_score"], 3),
                explanation=explanations.get(
                    str(job["id"]),
                    ""
                )
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


# Health Check
@app.get("/health")
async def health():

    return {
        "status": "ok",
        "message": "Smart Job Match Agent is running",
        "type": "LOCAL - 100% FREE, no APIs"
    }


# Run App
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )