"""
Simple embeddings using TF-IDF from scikit-learn.
- NO downloads
- NO API keys  
- Works on ANY computer
- 100% FREE
"""
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from typing import List

# Global vectorizer - created once
_vectorizer = None
_all_texts = []
_cache = {}


def initialize_vectorizer(all_job_texts: List[str], resume_text: str):
    """
    Initialize the TF-IDF vectorizer with all texts.
    This must be called once before ranking.
    
    Args:
        all_job_texts: List of all job descriptions
        resume_text: The resume text
    """
    global _vectorizer, _all_texts
    
    # Combine all texts for vocabulary
    _all_texts = [resume_text] + all_job_texts
    
    # Create vectorizer (this is free, no downloads)
    _vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words='english',
        max_features=1000,
        ngram_range=(1, 2)
    )
    
    # Fit on all texts
    _vectorizer.fit(_all_texts)


def get_embedding(text: str) -> List[float]:
    """
    Get TF-IDF embedding for text.
    Pure Python, NO downloads, NO APIs.
    
    Args:
        text: Text to embed
        
    Returns:
        Embedding vector as list
    """
    if _vectorizer is None:
        raise ValueError("Vectorizer not initialized. Call initialize_vectorizer first.")
    
    # Check cache
    cache_key = hash(text)
    if cache_key in _cache:
        return _cache[cache_key]
    
    # Transform text to TF-IDF vector
    vector = _vectorizer.transform([text]).toarray()[0]
    vector_list = vector.tolist()
    
    _cache[cache_key] = vector_list
    return vector_list


def prepare_job_text(job: dict) -> str:
    """Prepare job for embedding."""
    parts = [
        job.get("title", ""),
        ", ".join(job.get("skills", [])),
        job.get("description", ""),
        job.get("domain", ""),
    ]
    return " ".join([p for p in parts if p])


def prepare_resume_text(resume_data: dict) -> str:
    """Prepare resume for embedding."""
    parts = [
        ", ".join(resume_data.get("skills", [])),
        f"Experience: {resume_data.get('experience_years', 0)} years",
        "Roles: " + ", ".join(resume_data.get("preferred_roles", [])),
        resume_data.get("education", ""),
    ]
    return " ".join([p for p in parts if p])
