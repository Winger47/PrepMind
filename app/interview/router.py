from fastapi import APIRouter, Depends, HTTPException, WebSocket
from sqlalchemy.orm import Session
from app.auth.utils import get_current_user
from app.database import get_db
from app.interview.agent import get_session_questions, evaluate_answer, save_answer
from app.models import InterviewSession, InterviewQuestion, InterviewAnswer, User
from pydantic import BaseModel
from datetime import datetime
import json

router = APIRouter(prefix="/interview", tags=["interview"])


class start_session_request(BaseModel):
    jd_id: int


@router.post("/start")
def start_session(request: start_session_request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    interview_session = InterviewSession(
        user_id=current_user.id,
        jd_id=request.jd_id,
        status="active"
    )
    db.add(interview_session)
    db.commit()
    db.refresh(interview_session)
    return {"session_id": interview_session.id, "message": "Interview session started successfully"}


@router.websocket("/chat/{session_id}")
async def interview_chat(websocket: WebSocket, session_id: int):
    db = next(get_db())
    try:
        await websocket.accept()

        # Get session to know user_id
        session_obj = db.query(InterviewSession).filter(
            InterviewSession.id == session_id
        ).first()
        if not session_obj:
            await websocket.send_json({"error": "Session not found"})
            await websocket.close()
            return
        session_user_id = session_obj.user_id

        questions = get_session_questions(session_id, db)
        if not questions:
            await websocket.send_json({"error": "No questions found"})
            await websocket.close()
            return

        # Get already answered question IDs from DB
        previous_answers = db.query(InterviewAnswer).filter(
            InterviewAnswer.session_id == session_id
        ).all()
        answered_ids = {a.question_id for a in previous_answers}
        total_score = sum(a.score for a in previous_answers if a.score is not None)
        answered = len([a for a in previous_answers if a.score is not None])

        # Send welcome or resume message
        if answered_ids:
            await websocket.send_text(json.dumps({
                "type": "resume",
                "message": f"Resuming interview — {len(answered_ids)} questions already done",
                "remaining": len(questions) - len(answered_ids)
            }))
        else:
            await websocket.send_text(f"Welcome! Your interview has {len(questions)} questions. Let's begin!")

        for i, question in enumerate(questions):
            # Skip already answered questions
            if question.id in answered_ids:
                continue

            await websocket.send_text(json.dumps({
                "type": "question",
                "number": i + 1,
                "total": len(questions),
                "question": question.question,
                "difficulty": question.difficulty,
                "topic": question.topic
            }))
            while True:
                user_message = await websocket.receive_text()
                result = evaluate_answer(question.question, user_message)
                await websocket.send_text(json.dumps(result))

                if result.get("next"):
                    if result.get("type") == "answer":
                        total_score += result.get("score", 0)
                        answered += 1
                        save_answer(
                            session_id=session_id,
                            question_id=question.id,
                            user_id=session_user_id,
                            answer=user_message,
                            feedback=result.get("feedback", ""),
                            score=result.get("score", 0),
                            db=db
                        )
                    break

        avg_score = round(total_score / answered, 1) if answered > 0 else 0
        await websocket.send_text(json.dumps({
            "type": "complete",
            "message": "Interview complete!",
            "score": avg_score,
            "total_questions": len(questions),
            "answered": answered
        }))
        await websocket.close()
    finally:
        db.close()