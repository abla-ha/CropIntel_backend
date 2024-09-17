from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
from app.services.pest_service import predict_disease

router = APIRouter()

# Define the response model
class PredictionResponse(BaseModel):
    class_name: str
    confidence: float

@router.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    # Call the service function to make a prediction
    prediction = await predict_disease(file)
    return prediction