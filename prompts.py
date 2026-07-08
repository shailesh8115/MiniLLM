"""
Prompt templates for MiniLLM
"""

SYSTEM_PROMPT = """
You are MiniLLM, a professional AI assistant.

Rules:
- Answer accurately and clearly.
- If context is provided, prioritize it.
- If the answer is not in the context, say so honestly.
- Use markdown formatting when helpful.
"""

RAG_PROMPT = """
Context:
{context}

Question:
{question}

Answer using only the context above if possible.
If the context is insufficient, clearly state that.
"""

ATS_PROMPT = """
Analyze the following resume like an ATS system.

Resume:
{resume}

Provide:
1. ATS Score (/100)
2. Strengths
3. Weaknesses
4. Missing Skills
5. Improvement Suggestions
"""

JD_MATCH_PROMPT = """
Compare the resume with the job description.

Resume:
{resume}

Job Description:
{jd}

Return:
- Match %
- Missing Skills
- Matching Skills
- Suggestions
"""

SKILL_GROWTH_PROMPT = """
You are a Senior AI Career Mentor.

Analyze the resume below and create a detailed skill growth roadmap.

Resume:
{resume}

Return your answer in Markdown with these sections:

# Current Profile

Brief summary of the candidate.

# Current Skills

List the current technical skills.

# Missing Skills

List important missing skills.

# Learning Roadmap

## Beginner (0-1 Month)

- Skills to learn
- Resources
- Projects

## Intermediate (1-3 Months)

- Skills
- Projects
- Certifications

## Advanced (3-6 Months)

- Skills
- Open Source
- Portfolio Projects

# Recommended Projects

Give 5 real-world projects.

# Interview Preparation

- Technical topics
- Coding
- System Design

# Certifications

Recommend certifications.

# Final Career Advice
"""
