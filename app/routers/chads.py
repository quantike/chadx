
from fastapi import APIRouter
from loguru import logger

from app.dependencies import CHADX
from app.exchange.models import Chad

router = APIRouter(
    prefix="/chads",
    tags=["chads"],
    responses={404: {"description":  "not found"}}
)


@router.post("/campaign")
async def post_campaign(chad: Chad):
    # Update CHADX
    await CHADX.update(chad)
    logger.info(f"update chad: {chad.id}")

    return chad.id

@router.get("/campaign/{id}")
async def get_campaign(id: str):
    chad_or_none = await CHADX.get(id)

    return chad_or_none if chad_or_none else chad_or_none

