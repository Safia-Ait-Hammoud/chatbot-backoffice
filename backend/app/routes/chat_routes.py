from fastapi import APIRouter, Form
from services.chat.chat_service import ChatService

router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"],
)

@router.post("/")
async def chat(
    question: str = Form(...),
    project_id: str = Form(...),
):
    return await ChatService().chat(question, project_id)