# 1. imports
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.utils import get_current_user
from app.models import User
from app.research.agent import research_company
from pydantic import BaseModel

# 2. request schema
class ResearchRequest(BaseModel):
    company_name: str
    role: str

# 3. router
router = APIRouter(prefix="/research", tags=["research"])

# 4. endpoint
@router.post("/company")
def research(request: ResearchRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    results=research_company(current_user.id,request.company_name,request.role,db)
    return {"research": results.tips}