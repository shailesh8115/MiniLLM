"""
resume.py
------------------------------------
AI Resume Features for MiniLLM
Part 1
"""

import json
import re

from chatbot import bot

from prompts import (
    ATS_PROMPT,
    JD_MATCH_PROMPT,
    SKILL_GROWTH_PROMPT,
)


# ==========================================================
# Helper Function
# ==========================================================

def ask_llm(prompt: str) -> str:
    """
    Safe wrapper around bot.chat().
    Always returns a string.
    """

    try:

        response = bot.chat(prompt)

        if response is None:
            return "No response generated."

        if isinstance(response, str):
            return response

        if isinstance(response, (list, tuple)):
            return "\n".join(map(str, response))

        if isinstance(response, dict):
            return json.dumps(
                response,
                indent=4
            )

        return str(response)

    except Exception as e:

        return f"Error: {e}"


# ==========================================================
# ATS Resume Analysis
# ==========================================================

def analyze_resume(resume_text: str):

    prompt = ATS_PROMPT.format(
        resume=resume_text
    )

    return ask_llm(prompt)


# ==========================================================
# Resume Score
# ==========================================================

def resume_score(resume_text: str):

    prompt = f"""
You are an ATS Resume Expert.

Analyze the following resume.

Return in Markdown.

# ATS Score (/100)

# Professional Summary

# Strengths

# Weaknesses

# Missing Skills

# Missing Keywords

# Suggestions

Resume:

{resume_text}
"""

    return ask_llm(prompt)


# ==========================================================
# Resume Summary
# ==========================================================

def resume_summary(resume_text: str):

    prompt = f"""
Summarize this resume.

Return:

# Professional Summary

# Years of Experience

# Skills

# Education

# Projects

# Certifications

Resume:

{resume_text}
"""

    return ask_llm(prompt)


# ==========================================================
# Improve Resume
# ==========================================================

def improve_resume(resume_text: str):

    prompt = f"""
You are a Professional Resume Writer.

Rewrite this resume.

Requirements

• ATS Friendly

• Better formatting

• Strong action verbs

• Quantify achievements

• Professional summary

• Technical Skills

• Projects

• Experience

• Grammar correction

Resume

{resume_text}

Return ONLY the improved resume.
"""

    return ask_llm(prompt)


# ==========================================================
# Extract Resume Data
# ==========================================================

def extract_resume_data(resume_text):

    prompt = f"""
Extract the following information.

Return ONLY valid JSON.

{{
    "name":"",
    "email":"",
    "phone":"",
    "location":"",
    "summary":"",
    "skills":"",
    "experience":"",
    "education":"",
    "projects":"",
    "certifications":""
}}

Resume

{resume_text}
"""

    response = ask_llm(prompt)

    try:

        match = re.search(
            r"\{.*\}",
            response,
            re.DOTALL
        )

        if match:

            return json.loads(
                match.group()
            )

    except Exception:
        pass

    return {

        "name": "",

        "email": "",

        "phone": "",

        "location": "",

        "summary": "",

        "skills": "",

        "experience": "",

        "education": "",

        "projects": "",

        "certifications": ""

    }


# ==========================================================
# Extract Keywords
# ==========================================================

def extract_keywords(resume_text):

    prompt = f"""
Extract the most important ATS keywords.

Return comma separated keywords only.

Resume

{resume_text}
"""

    return ask_llm(prompt)
# ==========================================================
# Generate Resume
# ==========================================================

def generate_resume(data):
    """
    Generate an ATS-friendly resume from user data.
    """

    prompt = f"""
You are an expert ATS Resume Writer.

Create a professional one-page resume.

Candidate Information

Name:
{data.get("name","")}

Email:
{data.get("email","")}

Phone:
{data.get("phone","")}

Location:
{data.get("location","")}

LinkedIn:
{data.get("linkedin","")}

GitHub:
{data.get("github","")}

Education:
{data.get("education","")}

Experience:
{data.get("experience","")}

Skills:
{data.get("skills","")}

Projects:
{data.get("projects","")}

Requirements

- Professional Summary
- Technical Skills
- Experience
- Projects
- Education
- Certifications (if available)
- ATS Friendly
- Professional Formatting
- Strong Action Verbs
- Quantify achievements where possible

Return ONLY the resume.
"""

    return ask_llm(prompt)


# ==========================================================
# Job Description Match
# ==========================================================

def jd_match(resume_text, job_description):

    prompt = JD_MATCH_PROMPT.format(
        resume=resume_text,
        jd=job_description
    )

    return ask_llm(prompt)


# ==========================================================
# Skill Growth Roadmap
# ==========================================================

def skill_growth(resume_text):

    prompt = SKILL_GROWTH_PROMPT.format(
        resume=resume_text
    )

    return ask_llm(prompt)


# ==========================================================
# Cover Letter Generator
# ==========================================================

def generate_cover_letter(
    resume_text,
    job_description
):

    prompt = f"""
You are a professional career coach.

Using the resume and job description,
write a professional ATS-friendly cover letter.

Resume

{resume_text}

Job Description

{job_description}

Requirements

- One page
- Professional tone
- Mention relevant skills
- Highlight achievements
- End with a strong closing

Return ONLY the cover letter.
"""

    return ask_llm(prompt)


# ==========================================================
# Rewrite Resume
# ==========================================================

def rewrite_resume(
    resume_text,
    target_role
):

    prompt = f"""
Rewrite this resume specifically for the role below.

Target Role

{target_role}

Resume

{resume_text}

Requirements

- ATS Friendly
- Professional Summary
- Strong Bullet Points
- Include role-specific keywords
- Improve readability
- Better formatting
- Quantify achievements
- Modern resume style

Return ONLY the rewritten resume.
"""

    return ask_llm(prompt)


# ==========================================================
# Resume Headline
# ==========================================================

def generate_headline(resume_text):

    prompt = f"""
Generate five professional resume headlines.

Resume

{resume_text}

Return only the headlines.
"""

    return ask_llm(prompt)


# ==========================================================
# LinkedIn About
# ==========================================================

def linkedin_about(resume_text):

    prompt = f"""
Write a LinkedIn About section.

Resume

{resume_text}

Requirements

- 200-250 words
- Professional
- ATS Friendly
- Highlight achievements
- Include technical skills
"""

    return ask_llm(prompt)


# ==========================================================
# Interview Questions
# ==========================================================

def interview_questions(resume_text):

    prompt = f"""
Generate 20 interview questions and answers based on this resume.

Resume

{resume_text}

Return in Markdown format.

Each question should have a detailed answer.
"""

    return ask_llm(prompt)


# ==========================================================
# Skill Gap Analysis
# ==========================================================

def skill_gap_analysis(
    resume_text,
    job_description
):

    prompt = f"""
Compare the following resume with the job description.

Resume

{resume_text}

Job Description

{job_description}

Return the following sections.

# Match Percentage

# Matching Skills

# Missing Skills

# Missing Keywords

# Weak Areas

# Improvement Suggestions

# Learning Roadmap

# Final Recommendation
"""

    return ask_llm(prompt)
# ==========================================================
# Parse ATS Score
# ==========================================================

def extract_ats_score(report: str) -> int:
    """
    Extract ATS score from an AI response.
    """

    if not report:
        return 0

    patterns = [
        r'ATS\s*Score\s*[:\-]?\s*(\d{1,3})',
        r'(\d{1,3})\s*/\s*100',
        r'(\d{1,3})%'
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            report,
            re.IGNORECASE
        )

        if match:

            score = int(match.group(1))

            return max(0, min(score, 100))

    return 0


# ==========================================================
# Parse Match Percentage
# ==========================================================

def extract_match_percentage(report: str) -> int:

    if not report:
        return 0

    patterns = [
        r'Match\s*Percentage\s*[:\-]?\s*(\d{1,3})',
        r'(\d{1,3})%'
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            report,
            re.IGNORECASE
        )

        if match:

            value = int(match.group(1))

            return max(0, min(value, 100))

    return 0


# ==========================================================
# Markdown Cleaner
# ==========================================================

def clean_markdown(text: str):

    if not text:
        return ""

    text = text.replace("```markdown", "")
    text = text.replace("```", "")
    text = text.strip()

    return text


# ==========================================================
# Bullet Cleaner
# ==========================================================

def normalize_bullets(text: str):

    if not text:
        return ""

    text = text.replace("•", "-")
    text = text.replace("* ", "- ")

    return text


# ==========================================================
# Resume Validator
# ==========================================================

def validate_resume(text: str):

    if not text:
        return False, "Resume is empty."

    if len(text.strip()) < 100:
        return False, "Resume text is too short."

    return True, "Valid Resume"


# ==========================================================
# Safe AI Call
# ==========================================================

def safe_call(prompt):

    try:

        return ask_llm(prompt)

    except Exception as e:

        return f"Error: {e}"


# ==========================================================
# Exported Functions
# ==========================================================

__all__ = [

    "analyze_resume",

    "resume_score",

    "resume_summary",

    "improve_resume",

    "extract_resume_data",

    "extract_keywords",

    "generate_resume",

    "jd_match",

    "skill_growth",

    "generate_cover_letter",

    "rewrite_resume",

    "generate_headline",

    "linkedin_about",

    "interview_questions",

    "skill_gap_analysis",

    "extract_ats_score",

    "extract_match_percentage",

    "clean_markdown",

    "normalize_bullets",

    "validate_resume"

]