"""
Job matching and ranking logic.
"""

from typing import List, Dict

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from services.embeddings import (
    generate_embeddings_batch,
    create_job_text,
    create_resume_text
)


def rank_jobs(
    parsed_resume: dict,
    jobs: List[Dict],
    top_k: int = 5
) -> List[Dict]:
    """
    Rank jobs using cosine similarity.
    """

    # Resume text
    resume_text = create_resume_text(parsed_resume)

    # Job texts
    job_texts = [
        create_job_text(job)
        for job in jobs
    ]

    # Generate embeddings together
    all_embeddings = generate_embeddings_batch(
        [resume_text] + job_texts
    )

    resume_embedding = np.array(
        all_embeddings[0]
    ).reshape(1, -1)

    job_embeddings = np.array(
        all_embeddings[1:]
    )

    # Cosine similarity
    similarities = cosine_similarity(
        resume_embedding,
        job_embeddings
    )[0]

    ranked_jobs = []

    for idx, job in enumerate(jobs):

        ranked_job = job.copy()

        ranked_job["match_score"] = round(
            float(similarities[idx]) * 100,
            2
        )

        ranked_jobs.append(ranked_job)

    ranked_jobs.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return ranked_jobs[:top_k]