from fastapi import APIRouter

from chains.rag_chain import RAGChain
from api.schemas import ChatRequest, ChatResponse


router = APIRouter()

rag_chain = RAGChain()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    answer = rag_chain.ask(request.question)

    return ChatResponse(answer=answer)