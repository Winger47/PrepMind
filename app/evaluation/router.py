from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.utils import get_current_user
from app.models import User
from app.evaluation.agent import generate_report
import json

router = APIRouter(prefix="/evaluation", tags=["evaluation"])


@router.post("/report/{session_id}")
def create_report(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    report = generate_report(session_id, current_user.id, db)
    return {
        "session_id": report.session_id,
        "overall_score": report.overall_score,
        "total_questions": report.total_questions,
        "answered": report.answered,
        "strengths": json.loads(report.strengths),
        "weaknesses": json.loads(report.weaknesses),
        "topics_breakdown": json.loads(report.topics_breakdown),
        "study_plan": json.loads(report.study_plan),
        "recommendations": report.recommendations
    }