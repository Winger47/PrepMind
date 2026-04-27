from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class JobDescription(Base):
    __tablename__ = "job_descriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    jd_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CompanyResearch(Base):
    __tablename__ = "company_research"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    jd_id = Column(Integer, ForeignKey("job_descriptions.id"))
    role = Column(String, nullable=False)
    tech_stack = Column(String)
    company_name = Column(String, nullable=False)
    tips = Column(Text)
    culture = Column(Text)
    interview_process = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    research_id = Column(Integer, ForeignKey("company_research.id"))
    jd_id = Column(Integer, ForeignKey("job_descriptions.id"))
    company_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    question_type = Column(String, nullable=False)
    question = Column(Text, nullable=False)
    difficulty = Column(String)
    topic = Column(String)
    hints = Column(Text)
    ideal_answer = Column(Text)
    source = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
