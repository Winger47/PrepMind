from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text,Float
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

class InterviewAnswer(Base):
    __tablename__ = "interview_answers"

    id= Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("interview_questions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    answer = Column(Text, nullable=False)
    feedback = Column(Text)
    score = Column(Integer)  # 0-10
    created_at = Column(DateTime(timezone=True), server_default=func.now())     
    # add these columns:
    # id, session_id (FK to interview_sessions), question_id (FK to interview_questions)
    # user_id (FK to users), answer (Text), feedback (Text)
    # score (Integer 0-10), created_at
class InterviewSession(Base):
    __tablename__ = "interview_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    jd_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=False)
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

class InterviewReport(Base):
    __tablename__="interview_reports"
    id=Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    jd_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    overall_score = Column(Float)
    strengths = Column(Text)
    weaknesses = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    recommendations = Column(Text)
    topics_breakdown = Column(Text)
    total_questions = Column(Integer)
    answered = Column(Integer)
    study_plan = Column(Text)
    # add these columns:
