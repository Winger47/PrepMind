from groq import Groq
from tavily import TavilyClient
from fastapi import HTTPException
from sqlalchemy.orm import Session
import os
import json
from dotenv import load_dotenv

from app.models import CompanyResearch, InterviewQuestion, JobDescription

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def generate_questions(user_id: int, jd_id: int, db: Session):
    jd = (
        db.query(JobDescription)
        .filter(JobDescription.id == jd_id, JobDescription.user_id == user_id)
        .first()
    )
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")

    company_name = jd.company_name
    role = jd.role
    jd_text = jd.jd_text

    results = tavily_client.search(
        query=f"{company_name} {role} interview experience questions",
        max_results=10,
        include_domains=[
            "glassdoor.com",
            "reddit.com",
            "leetcode.com",
            "geeksforgeeks.org",
            "interviewbit.com",
            "blind.com",
            "medium.com",
        ],
    )
    content = "\n".join([r["content"] for r in results["results"]])

    research = (
        db.query(CompanyResearch)
        .filter(
            CompanyResearch.user_id == user_id,
            CompanyResearch.jd_id == jd.id,
        )
        .order_by(CompanyResearch.created_at.desc())
        .first()
    )

    research_text = research.tips if research else "No research available"
    research_id = research.id if research else None

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an expert interview coach who analyzes real interview experiences and the actual job description to generate authentic, role-specific interview questions.

Generate 15 interview questions across:
- 5 DSA, 4 System Design, 3 CS Fundamentals, 2 Behavioural, 1 Language Specific

For EACH question provide:
- type, question, difficulty, topic, hints, ideal_answer, source

Tailor topics, difficulty, and language-specific items to the responsibilities and required skills in the job description.

Return ONLY a valid JSON array. No explanation, no markdown.
Format: [{"type": "...", "question": "...", "difficulty": "...", "topic": "...", "hints": "...", "ideal_answer": "...", "source": "..."}]""",
            },
            {
                "role": "user",
                "content": (
                    f"Company: {company_name}\n"
                    f"Role: {role}\n\n"
                    f"Job Description:\n{jd_text}\n\n"
                    f"Research:\n{research_text}\n\n"
                    f"Real Experiences:\n{content}"
                ),
            },
        ],
    )

    questions = json.loads(response.choices[0].message.content)

    saved_questions = []
    for q in questions:
        question = InterviewQuestion(
            user_id=user_id,
            research_id=research_id,
            jd_id=jd.id,
            company_name=company_name,
            role=role,
            question_type=q["type"],
            question=q["question"],
            difficulty=q["difficulty"],
            topic=q["topic"],
            hints=q["hints"],
            ideal_answer=q["ideal_answer"],
            source=q["source"],
        )
        db.add(question)
        saved_questions.append(question)

    db.commit()

    return saved_questions
