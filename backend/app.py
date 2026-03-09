import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ml.analyze_resume import analyze_resume
from utils.resume_parser import extract_text_from_resume

app = FastAPI(title="AI Resume Analyzer")

# 1. Enhanced CORS: Critical for Flutter Web communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    # Updated to match your latest training result
    return {"status": "Backend Online", "accuracy": "93.69%"}

@app.post("/analyze-resume")
async def upload_resume(file: UploadFile = File(...)):
    # 2. Use UUID to prevent file name collisions if multiple people upload at once
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    temp_path = os.path.join(os.getcwd(), unique_filename)
    
    try:
        # Save the incoming file stream
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Step A: Extract text (supports PDF/DOCX)
        resume_text = extract_text_from_resume(temp_path)
        
        if not resume_text or len(resume_text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Could not extract meaningful text from file.")

        # Step B: Run the 93.69% Accuracy Pipeline
        analysis_results = analyze_resume(resume_text)
        return analysis_results

    except Exception as e:
        print(f"❌ Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal processing error.")
        
    finally:
        # Step C: Cleanup - Always delete the file after analysis
        if os.path.exists(temp_path):
            os.remove(temp_path)