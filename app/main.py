from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="PrepMind")

app.include_router(auth_router)

@app.get("/health")
def health():
    return {"status": "ok"}