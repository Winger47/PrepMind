from groq import Groq
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import InterviewSession, InterviewAnswer, InterviewQuestion, InterviewReport
import os
import json
from dotenv import load_dotenv

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_report(session_id: int, user_id: int, db: Session):
    # 1. Verify session
    session = db.query(InterviewSession).filter(
        InterviewSession.id == session_id,
        InterviewSession.user_id == user_id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # 2. Fetch all answers for this session
    answers = db.query(InterviewAnswer).filter(
        InterviewAnswer.session_id == session_id
    ).all()
    
    # 3. Build qa_list with question details
    qa_list = []
    for ans in answers:
        question = db.query(InterviewQuestion).filter(
            InterviewQuestion.id == ans.question_id
        ).first()
        qa_list.append({
            "question": question.question,
            "type": question.question_type,
            "topic": question.topic,
            "difficulty": question.difficulty,
            "user_answer": ans.answer,
            "score": ans.score,
            "feedback": ans.feedback
        })
    
    # 4. Calculate stats
    total_questions = len(qa_list)
    answered = len([qa for qa in qa_list if qa["score"] is not None])
    total_score = sum(qa["score"] for qa in qa_list if qa["score"] is not None)
    overall_score = round(total_score / answered, 1) if answered > 0 else 0
    
    # 5. Send to Groq for analysis
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """You are an expert technical interviewer and coach analyzing a mock interview.

Return ONLY valid JSON:
{
  "strengths": ["Topic 1", "Topic 2"],
  "weaknesses": ["Topic 3", "Topic 4"],
  "topic_breakdown": {
    "DSA": {"avg_score": 7.5, "feedback": "..."},
    "System Design": {"avg_score": 6.0, "feedback": "..."}
  },
  "study_plan": ["Day 1-2: ...", "Day 3-4: ..."],
  "recommendations": "Overall guidance..."
}"""
            },
            {
                "role": "user",
                "content": f"Overall Score: {overall_score}\n\nQ&A Data: {json.dumps(qa_list)}"
            }
        ]
    )
    analysis = json.loads(response.choices[0].message.content)
    
    # 6. Save report to DB
    report = InterviewReport(
        user_id=user_id,
        jd_id=session.jd_id,
        session_id=session_id,
        overall_score=overall_score,
        total_questions=total_questions,
        answered=answered,
        strengths=json.dumps(analysis.get("strengths", [])),
        weaknesses=json.dumps(analysis.get("weaknesses", [])),
        topics_breakdown=json.dumps(analysis.get("topic_breakdown", {})),
        study_plan=json.dumps(analysis.get("study_plan", [])),
        recommendations=analysis.get("recommendations", "")
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report