from groq import Groq
from tavily import TavilyClient
from fastapi import HTTPException
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from app.models import CompanyResearch, JobDescription

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def research_company(user_id: int, jd_id: int, db: Session):
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
        query=f"{company_name} {role} interview process tech stack culture",
        max_results=5,
    )
    content = "\n".join([r["content"] for r in results["results"]])

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a company research expert.
Analyze the search results AND the provided job description to produce a structured, role-specific report with:
1. Tech stack used (cross-reference the JD's required skills)
2. Interview process and style
3. Company culture
4. Preparation tips tailored to the JD's responsibilities and requirements
Be specific, actionable, and align your tips to the JD.""",
            },
            {
                "role": "user",
                "content": (
                    f"Company: {company_name}\n"
                    f"Role: {role}\n\n"
                    f"Job Description:\n{jd_text}\n\n"
                    f"Search Results:\n{content}"
                ),
            },
        ],
    )

    result = response.choices[0].message.content

    research = CompanyResearch(
        user_id=user_id,
        jd_id=jd.id,
        company_name=company_name,
        role=role,
        tips=result,
    )
    db.add(research)
    db.commit()
    db.refresh(research)

    return research
