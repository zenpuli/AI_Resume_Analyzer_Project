from fastapi import APIRouter
from pydantic import BaseModel

from ml.predict_roles import predict_top_3_roles

router = APIRouter(prefix="/model-test", tags=["Model Testing"])


class ResumeRequest(BaseModel):
    resume_text: str


@router.post("/predict")
def test_model(data: ResumeRequest):
    resume_text = data.resume_text

    predictions = predict_top_3_roles(resume_text)

    return {
        "predictions": predictions
    }