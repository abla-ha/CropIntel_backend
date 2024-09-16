import pandas as pd
from app.schemas.crop import CropRecommendationRequest, CropRecommendationResponse
import joblib
import requests
from app.core.config import LLM_API_URL 

# Load the model, scaler, and label encoder
model = joblib.load('app/services/model/crop_recommendation_model.pkl')
scaler = joblib.load('app/services/model/scaler.pkl')
label_encoder = joblib.load('app/services/model/label_encoder.pkl')


def get_llm_report(previous_crop: str, recommended_crop: str, input_data: dict) -> str:
    """
    Sends a prompt to the LLM service to generate a detailed report based on the previous crop and 
    the predicted crop.
    """
    # Craft the prompt based on input data
    prompt = f"""
    Previous crop: {previous_crop}
    Recommended crop: {recommended_crop}
    Farming conditions:
    - Nitrogen: {input_data['N']}
    - Phosphorus: {input_data['P']}
    - Potassium: {input_data['K']}
    - Temperature: {input_data['temperature']}°C
    - Humidity: {input_data['humidity']}%
    - pH: {input_data['ph']}
    - Rainfall: {input_data['rainfall']} mm

    Based on these details, please generate a comprehensive report on the best crop to farm and any recommendations for improving yield or crop health.
    """


    # Create the payload including the prompt under 'userInput'
    payload = {
        "userInput": prompt
    }

    # Call the LLM service with the crafted payload
    response = requests.post(LLM_API_URL, json=payload)
    print("LLM service response:", response.text) 

    # Handle the LLM response
    if response.status_code == 200:
        llm_result = response.json()["generated_text"]
        return llm_result
    else:
        raise Exception(f"Error from LLM service: {response.status_code} - {response.text}")


def recommend_crop(data: CropRecommendationRequest, previous_crop: str) -> CropRecommendationResponse:
    # Convert input data to a DataFrame (excluding 'previous_crop')
    input_data = pd.DataFrame([data.dict(exclude={'previous_crop'})])

    # Ensure the order of features is correct
    input_data = input_data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]

    # Scale the input data
    scaled_data = scaler.transform(input_data)

    # Make a prediction
    prediction = model.predict(scaled_data)

    # Decode the prediction
    decoded_prediction = label_encoder.inverse_transform(prediction)[0]

    # Get a detailed report from the LLM by calling the get_llm_report function
    report = get_llm_report(previous_crop, decoded_prediction, data.dict())

    # Return the recommended crop and the LLM-generated report
    return CropRecommendationResponse(recommended_crop=decoded_prediction, llm_report=report)
