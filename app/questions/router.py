from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.auth.utils import get_current_user
from app.models import User
from app.questions.agent import generate_questions


class QuestionRequest(BaseModel):
    jd_id: int


router = APIRouter(prefix="/questions", tags=["questions"])

@router.post("/generate")  # ← correct
def generate(
    request: QuestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    questions = generate_questions(current_user.id, request.jd_id, db)
    return {
        "questions": [
            {
                "id": q.id,
                "type": q.question_type,
                "question": q.question,
                "difficulty": q.difficulty,
                "topic": q.topic,
                "hints": q.hints,
                "ideal_answer": q.ideal_answer,
                "source": q.source,
            }
            for q in questions
        ]
    }
@router.get("/list")
def list_questions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from app.models import InterviewQuestion
    questions = db.query(InterviewQuestion).filter(
        InterviewQuestion.user_id == current_user.id
    ).all()
    return {
        "count": len(questions),
        "questions": [{"id": q.id, "type": q.question_type, "question": q.question, "difficulty": q.difficulty} for q in questions]
    }

