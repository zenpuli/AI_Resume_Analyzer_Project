from fastapi import APIRouter
from pydantic import BaseModel

from ml.predict_roles import predict_top_3_roles

router = APIRouter(prefix="/screen2", tags=["Resume ML Prediction"])


class ResumeRequest(BaseModel):
    resume_text: str


@router.post("/predict")
def predict_roles(data: ResumeRequest):
    resume_text = data.resume_text

    predictions = predict_top_3_roles(resume_text)

    return {
        "top_3_predictions": predictions
    }