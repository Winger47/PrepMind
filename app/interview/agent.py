from fastapi import HTTPException
from groq import Groq
from sqlalchemy.orm import Session
from app.models import InterviewSession, InterviewQuestion, InterviewAnswer
import os
import json
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_session_questions(session_id: int, db: Session):
    session = db.query(InterviewSession).filter(
        InterviewSession.id == session_id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    questions = db.query(InterviewQuestion).filter(
        InterviewQuestion.jd_id == session.jd_id
    ).all()
    return questions


def evaluate_answer(question: str, user_message: str) -> dict:
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an expert technical interviewer and coach conducting a mock interview.

The candidate will either:
1. Answer the interview question
2. Ask a clarifying question or request a hint
3. Explicitly ask for the full answer

For ANSWERS return:
{"type": "answer", "score": 0-10, "feedback": "detailed feedback", "encouragement": "motivating sentence", "next": true}

For QUESTIONS/HINTS return:
{"type": "question", "response": "helpful hint without full answer", "encouragement": "encourage to try", "next": false}

For REVEAL return:
{"type": "reveal", "answer": "complete answer", "learning": "key concepts", "next": true}

Return ONLY valid JSON, no markdown, no explanation."""
            },
            {
                "role": "user",
                "content": f"Interview Question: {question}\n\nCandidate Message: {user_message}"
            }
        ]
    )
    try:
        result = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        result = {
            "type": "answer",
            "score": 0,
            "feedback": response.choices[0].message.content,
            "encouragement": "Keep trying!",
            "next": True
        }
    return result


def save_answer(session_id: int, question_id: int, user_id: int,
                answer: str, feedback: str, score: int, db: Session):
    interview_answer = InterviewAnswer(
        session_id=session_id,
        question_id=question_id,
        user_id=user_id,
        answer=answer,
        feedback=feedback,
        score=score
    )
    db.add(interview_answer)
    db.commit()
    db.refresh(interview_answer)
    return interview_answer