from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.jd.router import router as jd_router
from app.research.router import router as research_router
from app.questions.router import router as questions_router
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="PrepMind")

app.include_router(auth_router)
app.include_router(jd_router)
app.include_router(research_router)
app.include_router(questions_router)


@app.get("/health")
def health():
    return {"status": "ok"}
