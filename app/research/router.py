from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.auth.utils import get_current_user
from app.models import User
from app.research.agent import research_company


class ResearchRequest(BaseModel):
    jd_id: int


router = APIRouter(prefix="/research", tags=["research"])


@router.post("/company")
def research(
    request: ResearchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    results = research_company(current_user.id, request.jd_id, db)
    return {"research": results.tips}
