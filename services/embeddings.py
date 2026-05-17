"""
Lightweight TF-IDF based embeddings using scikit-learn.
Completely local and deployment friendly.
"""

from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer

# Global vectorizer
vectorizer = TfidfVectorizer(stop_words="english")


def generate_embedding(text: str) -> List[float]:
    """
    Generate TF-IDF embedding for single text.
    """

    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    embedding = vectorizer.fit_transform([text])

    return embedding.toarray()[0].tolist()


def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """
    Generate TF-IDF embeddings for multiple texts.
    """

    if not texts:
        raise ValueError("Texts list cannot be empty")

    valid_texts = [
        t.strip()
        for t in texts
        if t and t.strip()
    ]

    if not valid_texts:
        raise ValueError("No valid texts")

    embeddings = vectorizer.fit_transform(valid_texts)

    return embeddings.toarray().tolist()


def create_job_text(job: dict) -> str:
    """
    Convert job into searchable text.
    """

    title = job.get("title", "")
    skills = " ".join(job.get("skills", []))
    description = job.get("description", "")
    domain = job.get("domain", "")

    combined = (
        f"{title}. "
        f"Skills: {skills}. "
        f"Domain: {domain}. "
        f"{description}"
    )

    return combined.strip()


def create_resume_text(parsed_resume: dict) -> str:
    """
    Convert parsed resume into searchable text.
    """

    skills = " ".join(parsed_resume.get("skills", []))

    preferred_roles = " ".join(
        parsed_resume.get("preferred_roles", [])
    )

    education = parsed_resume.get("education", "")

    experience = parsed_resume.get(
        "experience_years",
        0
    )

    combined = (
        f"Skills: {skills}. "
        f"Preferred roles: {preferred_roles}. "
        f"Education: {education}. "
        f"Experience: {experience} years."
    )

    return combined.strip()