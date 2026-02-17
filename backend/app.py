from fastapi import FastAPI
from screen1.router import router as screen1_router
from screen2.router import router as screen2_router

app = FastAPI(title="AI Resume Analyzer")

app.include_router(screen1_router)
app.include_router(screen2_router)

@app.get("/")
def root():
    return {"status": "Backend running successfully"}
