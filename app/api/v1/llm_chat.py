from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llm_service import run_chat

router = APIRouter()

class ChatRequest(BaseModel):
    userInput: str

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = await run_chat(request.userInput)
        if response.startswith("Error:"):
            if "blocked due to safety concerns" in response:
                raise HTTPException(status_code=400, detail=response)
            else:
                raise HTTPException(status_code=500, detail=response)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))