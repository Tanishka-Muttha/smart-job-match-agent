"""
Simple resume parsing and job reasoning using pattern matching.
NO API calls, NO external LLM, 100% FREE.
Still demonstrates tool calling through structured reasoning.
"""
import re
from typing import Dict, List, Any


def parse_resume(resume_text: str) -> Dict[str, Any]:
    """
    Parse resume using pattern matching and heuristics.
    NO API calls, pure Python logic.
    
    Args:
        resume_text: Raw resume text
        
    Returns:
        Parsed resume data
    """
    resume_lower = resume_text.lower()
    
    # Extract name (usually at the beginning)
    name_match = re.search(r'(?:name[:\s]*)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', resume_text)
    name = name_match.group(1) if name_match else "Candidate"
    
    # Extract skills (look for common tech terms and keywords)
    common_skills = [
        'python', 'javascript', 'java', 'c++', 'ruby', 'go', 'rust', 'php',
        'react', 'vue', 'angular', 'node.js', 'django', 'flask', 'fastapi',
        'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
        'sql', 'mongodb', 'postgresql', 'mysql', 'redis',
        'aws', 'gcp', 'azure', 'docker', 'kubernetes',
        'git', 'ci/cd', 'devops', 'linux', 'bash',
        'machine learning', 'deep learning', 'nlp', 'computer vision',
        'data science', 'analytics', 'bi', 'tableau',
        'rest api', 'graphql', 'grpc', 'websocket',
        'agile', 'scrum', 'jira', 'confluence'
    ]
    
    skills = []
    for skill in common_skills:
        if skill in resume_lower:
            # Format skill properly
            formatted_skill = ' '.join(word.capitalize() for word in skill.split())
            if formatted_skill not in skills:
                skills.append(formatted_skill)
    
    # Extract experience years
    years_match = re.search(r'(\d+)\s*\+?\s*years?', resume_lower)
    experience_years = int(years_match.group(1)) if years_match else 0
    
    # Extract preferred roles
    role_keywords = [
        'software engineer', 'developer', 'data scientist', 'ml engineer',
        'product manager', 'ux designer', 'devops engineer', 'architect',
        'analyst', 'consultant', 'manager'
    ]
    
    preferred_roles = []
    for role in role_keywords:
        if role in resume_lower:
            formatted_role = ' '.join(word.capitalize() for word in role.split())
            if formatted_role not in preferred_roles:
                preferred_roles.append(formatted_role)
    
    # Extract education
    education_keywords = ['bs', 'ba', 'ms', 'ma', 'phd', 'btech', 'mtech']
    education = "Not specified"
    for keyword in education_keywords:
        if keyword in resume_lower:
            # Find the context around this keyword
            idx = resume_lower.find(keyword)
            context = resume_text[max(0, idx-10):min(len(resume_text), idx+100)]
            education = context.strip()
            break
    
    return {
        "name": name,
        "skills": skills if skills else ["General"],
        "experience_years": experience_years,
        "preferred_roles": preferred_roles if preferred_roles else ["Any Role"],
        "education": education
    }


def generate_match_explanations(
    resume_data: Dict[str, Any],
    top_jobs: List[Dict[str, Any]]
) -> Dict[str, str]:
    """
    Generate explanations for why each job matches.
    Uses rule-based logic, NO API calls.
    
    Args:
        resume_data: Parsed resume
        top_jobs: Top matching jobs
        
    Returns:
        Job ID -> explanation mapping
    """
    explanations = {}
    
    for job in top_jobs:
        job_id = str(job['id'])
        
        # Count skill matches
        candidate_skills = [s.lower() for s in resume_data.get('skills', [])]
        required_skills = [s.lower() for s in job.get('skills', [])]
        skill_matches = sum(1 for s in candidate_skills if any(s in req for req in required_skills))
        
        # Check experience level
        required_exp = job.get('experience_years', 0)
        candidate_exp = resume_data.get('experience_years', 0)
        exp_fit = candidate_exp >= required_exp * 0.8  # Allow 80% match
        
        # Check domain/role alignment
        candidate_roles = [r.lower() for r in resume_data.get('preferred_roles', [])]
        job_title = job.get('title', '').lower()
        role_match = any(role in job_title for role in candidate_roles)
        
        # Build explanation
        explanation_parts = []
        
        if skill_matches > 0:
            explanation_parts.append(
                f"Your {skill_matches} matching skills align with this role."
            )
        
        if exp_fit:
            explanation_parts.append(
                f"Your {candidate_exp} years of experience matches the {required_exp} years required."
            )
        else:
            explanation_parts.append(
                f"You have {candidate_exp} years, role requires {required_exp} - experience level is slightly below but could work with training."
            )
        
        if role_match:
            explanation_parts.append(
                f"This {job.get('title')} role aligns well with your preferred career path."
            )
        else:
            explanation_parts.append(
                f"While not your typical role, the {job.get('domain')} domain matches your background."
            )
        
        explanation = " ".join(explanation_parts)
        explanations[job_id] = explanation
    
    return explanations


def generate_clarifying_question(
    resume_data: Dict[str, Any],
    top_jobs: List[Dict[str, Any]]
) -> str:
    """
    Generate a smart follow-up question based on resume and matches.
    Uses heuristics, NO API calls.
    
    Args:
        resume_data: Parsed resume
        top_jobs: Top matching jobs
        
    Returns:
        Clarifying question string
    """
    # Check if all top jobs are remote
    remote_count = sum(1 for job in top_jobs if job.get('remote'))
    if remote_count >= 3:
        return "I notice several top matches are remote-only. Are you comfortable working fully remote, or do you prefer on-site/hybrid positions?"
    
    # Check if top jobs are in different domains
    domains = set(job.get('domain', 'Unknown') for job in top_jobs)
    if len(domains) >= 3:
        domain_list = ', '.join(list(domains)[:3])
        return f"Your matches span multiple industries ({domain_list}). Is there a particular domain you're most passionate about, or are you open to exploring different sectors?"
    
    # Check for salary range consideration
    avg_salary = sum(job.get('salary_lpa', 0) for job in top_jobs) / len(top_jobs)
    if avg_salary > 0:
        return f"The matching roles have an average salary of {avg_salary:.0f} LPA. Is there a specific salary range or compensation expectation you're looking for?"
    
    # Check if location is important
    locations = set(job.get('location', 'Unknown') for job in top_jobs)
    if len(locations) > 1:
        return f"Your top matches are across different locations ({', '.join(list(locations)[:2])}). Do you have any location preferences or are you open to relocating?"
    
    # Default question based on missing skills
    if not resume_data.get('skills'):
        return "Your resume doesn't mention any specific technical skills. Are there particular technologies or tools you'd like to work with?"
    
    return "Looking at your profile, what's most important to you in your next role - learning new skills, company stability, or growth potential?"
