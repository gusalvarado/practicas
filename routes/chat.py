from fastapi import APIRouter
from pydantic import BaseModel
from services.idea_expander import IdeaExpander

class MessageRequest(BaseModel):
    message: str
    session_id: str

router = APIRouter()
expander = IdeaExpander()

@router.post("/chat")
async def chat(request: MessageRequest):
    try:
        reply = expander.expand(request.message)
        return {"reply": reply}
    except Exception as e:
        return {"error": str(e)}