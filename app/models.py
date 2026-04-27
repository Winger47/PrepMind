from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
class CompanyResearch(Base):
    __tablename__ = "company_research"  # 4 spaces
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False)
    tech_stack = Column(String)
    company_name = Column(String, nullable=False)
    tips = Column(Text)
    culture = Column(Text)
    interview_process = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
