from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from typing import List

from app.exchange.embedder import Embedder


router = APIRouter(prefix="/embed", tags=["embed"])

embedder = Embedder()  # Initialize the embedder


class EmbedRequest(BaseModel):
    chunks: List[str]


@router.post("/")
async def generate_embeddings(request: EmbedRequest):
    try:
        embeddings = embedder.embed(request.chunks)
        return {"embeddings": embeddings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
