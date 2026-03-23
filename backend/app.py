import os
import uuid
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ml.analyze_resume import analyze_resume
from utils.resume_parser import extract_text_from_resume

app = FastAPI(title="AI Resume Analyzer")

# 1. Enhanced CORS: Optimized for Firebase Hosting & Render communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    """ Health check for Render deployment """
    return {
        "status": "Backend Online", 
        "accuracy": "93.69%",
        "message": "Ready for Resume Analysis"
    }

@app.post("/analyze-resume")
async def upload_resume(file: UploadFile = File(...)):
    # 2. Use UUID to prevent file name collisions
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    temp_path = os.path.join(os.getcwd(), unique_filename)
    
    try:
        # Save the incoming file stream
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Step A: Extract text
        resume_text = extract_text_from_resume(temp_path)
        
        if not resume_text or len(resume_text.strip()) < 10:
            return {"error": "provide a valid resume"}

        # Step B: Run the 93.69% Accuracy Pipeline
        analysis_results = analyze_resume(resume_text)
        
        if isinstance(analysis_results, dict) and "error" in analysis_results:
             return analysis_results

        return analysis_results

    except Exception as e:
        print(f"❌ Server Error: {str(e)}")
        return {"error": "Internal processing error. Check file format."}
        
    finally:
        # Step C: Cleanup
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass