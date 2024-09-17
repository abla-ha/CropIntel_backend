# /schemas/pest_disease.py

from pydantic import BaseModel

class PredictionResponse(BaseModel):
    class_name: str
    confidence: float
