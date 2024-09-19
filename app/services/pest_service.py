# /services/pest_service.py

from fastapi import UploadFile
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import tarfile
import os

# Define the path to the tar.gz file and the directory to extract to
tar_path = 'app/services/model/model.tar.gz'
extract_to = 'app/services/model/'

# Extract the tar.gz file
if not os.path.exists(extract_to):
    os.makedirs(extract_to)

with tarfile.open(tar_path, 'r:gz') as tar:
    tar.extractall(path=extract_to)



# Load the model once when the module is imported
model = tf.keras.models.load_model('app/services/model/trained_plant_disease_model.keras')

# List of class names as defined in training
class_names = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy',
    'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
    'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy',
    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
    'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot',
    'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

async def predict_disease(file: UploadFile):
    # Read and preprocess the image
    img = Image.open(io.BytesIO(await file.read()))
    img = img.resize((128, 128))  # Resize to the size the model expects

    # Convert to numpy array and normalize
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    # Make a prediction using the model
    predictions = model.predict(img_array)
    predicted_index = np.argmax(predictions, axis=1)[0]
    confidence = np.max(predictions, axis=1)[0]

    # Get the class name from the list
    class_name = class_names[predicted_index]

    return {"class_name": class_name, "confidence": float(confidence)}
