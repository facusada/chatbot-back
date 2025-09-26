from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_chat_service
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService, ChatServiceError

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def create_chat_completion(
    payload: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    try:
        response = await chat_service.generate_reply(
            session_id=payload.session_id,
            messages=payload.messages,
            context=payload.context,
        )
    except ChatServiceError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return response
