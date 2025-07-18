from fastapi import APIRouter
from pydantic import BaseModel
from services.idea_expander import IdeaExpander

routes = APIRouter()
expander = IdeaExpander()

class IdeaRequest(BaseModel):
  idea: str

@routes.post("/expand")
async def expand_idea(request: IdeaRequest):
  expanded = expander.expand(request.idea)
  return {"expanded_idea": expanded}