from fastapi import APIRouter, HTTPException, Query
from app.schemas.crop import CropRecommendationRequest, CropRecommendationResponse
from app.services.crop_service import recommend_crop

router = APIRouter()

@router.post("/recommend", response_model=CropRecommendationResponse)
def recommend_crop_route(
    data: CropRecommendationRequest,
    previous_crop: str = Query(..., description="The previous crop used for comparison")
):
    try:
        # Call the crop recommendation service
        result = recommend_crop(data, previous_crop)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
