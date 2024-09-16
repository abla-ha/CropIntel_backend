from pydantic import BaseModel

# Request model for crop recommendation
class CropRecommendationRequest(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float
  

# Response model for crop recommendation
class CropRecommendationResponse(BaseModel):
    recommended_crop: str
    llm_report: str  
