from fastapi import FastAPI
from screen2.router import router as screen2_router

app = FastAPI(title="AI Resume Analyzer")
app.include_router(screen2_router)

@app.get("/")
def root():
    return {"status": "Backend running successfully"}
