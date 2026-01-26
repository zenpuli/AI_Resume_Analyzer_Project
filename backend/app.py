# backend/app.py

from fastapi import FastAPI
from pydantic import BaseModel
from ml.analyze_resume import analyze_resume

app = FastAPI(title="AI Resume Analyzer")

class ResumeRequest(BaseModel):
    resume_text: str

@app.post("/analyze")
def analyze(request: ResumeRequest):
    return analyze_resume(request.resume_text)

@app.get("/")
def health():
    return {"status": "Backend running"}
