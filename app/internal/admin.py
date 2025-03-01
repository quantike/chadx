from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def health():
    return {"message": "all systems go"}
