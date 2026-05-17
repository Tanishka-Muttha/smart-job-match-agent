"""
Job matcher using cosine similarity on TF-IDF embeddings.
100% FREE, pure Python, NO API calls.
"""
from typing import List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from services.embeddings import get_embedding, prepare_job_text, prepare_resume_text, initialize_vectorizer


def rank_jobs(
    resume_data: dict,
    jobs: List[dict],
    top_n: int = 5
) -> List[dict]:
    """
    Rank jobs by semantic similarity to resume.
    Completely FREE - pure Python, no APIs.
    
    Args:
        resume_data: Parsed resume
        jobs: List of job dicts
        top_n: Number of top jobs to return
        
    Returns:
        Top-N jobs with similarity scores
    """
    # Prepare texts
    resume_text = prepare_resume_text(resume_data)
    job_texts = [prepare_job_text(job) for job in jobs]
    
    # Initialize vectorizer with all texts (one-time setup)
    initialize_vectorizer(job_texts, resume_text)
    
    # Get embeddings
    resume_embedding = np.array(get_embedding(resume_text)).reshape(1, -1)
    job_embeddings = np.array([get_embedding(text) for text in job_texts])
    
    # Compute cosine similarity
    similarities = cosine_similarity(resume_embedding, job_embeddings)[0]
    
    # Create results
    results = []
    for job, score in zip(jobs, similarities):
        results.append({
            **job,
            "similarity_score": float(score)
        })
    
    # Sort by score
    results.sort(key=lambda x: x["similarity_score"], reverse=True)
    
    return results[:top_n]
