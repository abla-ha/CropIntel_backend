import os
from dotenv import load_dotenv
from google.generativeai import GenerativeModel, configure
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import google.generativeai as genai



load_dotenv()

API_KEY = os.getenv("API_KEY")
MODEL_NAME = "gemini-pro"

# Configure the library
configure(api_key=API_KEY)

async def run_chat(user_input: str) -> str:
    try:
        # Create a GenerativeModel instance
        model = GenerativeModel(MODEL_NAME)

        generation_config = {
            "temperature": 0.9,
            "top_k": 1,
            "top_p": 1,
            "max_output_tokens": 1000,
        }


        # Start a chat session
        chat = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": ["You are an agriculture expert assistant named AgriBot. Only provide information related to agriculture, such as crops, harvests, plant diseases, soil management, etc. Politely refuse to answer any unrelated questions."],
                },
                {
                    "role": "model",
                    "parts": ["Hello! I'm AgriBot, your agriculture assistant. How can I help you today?"],
                },
            ],
        )

        # Send the user's message and get the response
        response = chat.send_message(
            user_input,
            generation_config=generation_config,
    
        )
        
        return response.text

    except genai.types.BlockedPromptException as e:
        print(f"BlockedPromptException: {str(e)}")
        return f"Error: The input was blocked due to safety concerns. Please rephrase your question."
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return f"Error: {str(e)}"

# Print model information for debugging
print(f"Available models:")
for m in genai.list_models():
    print(f"Model name: {m.name}")
    print(f"Model description: {m.description}")
    print(f"Input token limit: {m.input_token_limit}")
    print(f"Output token limit: {m.output_token_limit}")
    print(f"Supported generation methods: {m.supported_generation_methods}")
    print("---")