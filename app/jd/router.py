from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.auth.utils import get_current_user
from app.models import (
    JobDescription,
    User,
    CompanyResearch,
    InterviewQuestion,
    InterviewSession,
    InterviewAnswer,
    InterviewReport,
)


class JDUploadRequest(BaseModel):
    company_name: str
    role: str
    jd_text: str


router = APIRouter(prefix="/jd", tags=["jd"])


@router.post("/upload")
def upload_jd(
    request: JDUploadRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    jd = JobDescription(
        user_id=current_user.id,
        company_name=request.company_name,
        role=request.role,
        jd_text=request.jd_text,
    )
    db.add(jd)
    db.commit()
    db.refresh(jd)
    return {"jd_id": jd.id, "message": "Job description uploaded successfully"}


@router.get("/list")
def list_jds(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    jds = (
        db.query(JobDescription)
        .filter(JobDescription.user_id == current_user.id)
        .order_by(JobDescription.created_at.desc())
        .all()
    )
    return {
        "job_descriptions": [
            {
                "id": jd.id,
                "company_name": jd.company_name,
                "role": jd.role,
                "jd_text": jd.jd_text,
                "created_at": jd.created_at,
            }
            for jd in jds
        ]
    }


@router.get("/{jd_id}")
def get_jd(
    jd_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    jd = (
        db.query(JobDescription)
        .filter(
            JobDescription.id == jd_id,
            JobDescription.user_id == current_user.id,
        )
        .first()
    )
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
    return {
        "id": jd.id,
        "company_name": jd.company_name,
        "role": jd.role,
        "jd_text": jd.jd_text,
        "created_at": jd.created_at,
    }


@router.delete("/{jd_id}")
def delete_jd(
    jd_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    jd = (
        db.query(JobDescription)
        .filter(
            JobDescription.id == jd_id,
            JobDescription.user_id == current_user.id,
        )
        .first()
    )
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")

    # Clean up child rows that reference this JD (no ON DELETE CASCADE in schema).
    session_ids = [
        s.id for s in db.query(InterviewSession.id).filter(InterviewSession.jd_id == jd_id).all()
    ]
    if session_ids:
        db.query(InterviewAnswer).filter(InterviewAnswer.session_id.in_(session_ids)).delete(synchronize_session=False)
        db.query(InterviewReport).filter(InterviewReport.session_id.in_(session_ids)).delete(synchronize_session=False)
        db.query(InterviewSession).filter(InterviewSession.id.in_(session_ids)).delete(synchronize_session=False)
    db.query(InterviewQuestion).filter(InterviewQuestion.jd_id == jd_id).delete(synchronize_session=False)
    db.query(CompanyResearch).filter(CompanyResearch.jd_id == jd_id).delete(synchronize_session=False)

    db.delete(jd)
    db.commit()
    return {"message": "Job description deleted successfully"}
