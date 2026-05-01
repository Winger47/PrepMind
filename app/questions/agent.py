from groq import Groq
from fastapi import HTTPException
from sqlalchemy.orm import Session
import os
import json
import uuid
from dotenv import load_dotenv

from app.models import CompanyResearch, InterviewQuestion, JobDescription
from app.rag.vector_store import search_similar_questions, add_questions

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_questions(user_id: int, jd_id: int, db: Session):
    # Step 1: Fetch JD from DB
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
    
    # Step 2: RAG retrieval — find similar questions from bank
    rag_query = f"{company_name} {role} {jd_text[:500]}"  # use first 500 chars of JD
    rag_results = search_similar_questions(rag_query, n=10)
    
    similar_questions = rag_results["documents"][0] if rag_results["documents"] else []
    rag_context = "\n".join([f"- {q}" for q in similar_questions])
    
    # Step 3: Fetch research if exists
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
    
    # Step 4: Generate questions using Groq with RAG context
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """You are an expert interview coach who generates authentic, role-specific interview questions.

You will receive:
1. A job description
2. Company research
3. Reference questions from our curated question bank (these are real questions from past interviews)

Use the reference questions as INSPIRATION for style and depth. Generate 15 NEW questions tailored to this specific JD — do not copy reference questions verbatim.

Generate 15 interview questions across:
- 5 DSA, 4 System Design, 3 CS Fundamentals, 2 Behavioural, 1 Language Specific

For EACH question provide:
- type, question, difficulty, topic, hints, ideal_answer, source

Return ONLY valid JSON object with a "questions" key containing the array.
Format: {"questions": [{"type": "...", "question": "...", "difficulty": "...", "topic": "...", "hints": "...", "ideal_answer": "...", "source": "..."}]}""",
            },
            {
                "role": "user",
                "content": (
                    f"Company: {company_name}\n"
                    f"Role: {role}\n\n"
                    f"Job Description:\n{jd_text}\n\n"
                    f"Research:\n{research_text}\n\n"
                    f"Reference Questions from Bank:\n{rag_context}"
                ),
            },
        ],
    )
    
    parsed = json.loads(response.choices[0].message.content)
    questions = parsed.get("questions", [])
    
    # Step 5: Save to PostgreSQL AND ChromaDB
    saved_questions = []
    rag_questions_to_add = []
    
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
        
        # Prepare for ChromaDB (grow the bank over time)
        rag_questions_to_add.append({
            "id": f"gen_{uuid.uuid4().hex[:8]}",
            "text": q["question"],
            "metadata": {
                "company": company_name,
                "type": q["type"],
                "topic": q["topic"],
                "difficulty": q["difficulty"]
            }
        })
    
    db.commit()
    
    # Step 6: Add new questions to ChromaDB bank for future RAG
    if rag_questions_to_add:
        add_questions(rag_questions_to_add)
    
    return saved_questions