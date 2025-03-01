
from typing import List

from fastapi import APIRouter
from loguru import logger

from app.dependencies import CHADX
from app.exchange.models import Beta, Chad

router = APIRouter(
    prefix="/chads",
    tags=["chads"],
    responses={404: {"description":  "not found"}}
)


@router.post("/campaign")
async def post_campaign(chad: Chad):
    # Update CHADX
    await CHADX.put(chad)
    logger.info(f"put chad: {chad.id}")

    return chad.id

@router.post("/campaign/batch")
async def post_campaign_batch(chads: List[Chad]):
    # Update CHADX
    for chad in chads:
        await CHADX.put(chad)
        logger.info(f"put chad: {chad.id}")

    return [chad.id for chad in chads]

@router.get("/campaign/{id}")
async def get_campaign(id: str):
    chad_or_none = await CHADX.get(id)

    return chad_or_none if chad_or_none else chad_or_none

@router.delete("/campaign/{id}")
async def delete_campaign(id: str):
    id_or_none = await CHADX.delete(id)

    return id_or_none if id_or_none else id_or_none

@router.get("/match")
async def get_match(prompt: str):
    """
    Accepts a prompt via a query parameter, creates a Beta instance, 
    and then uses the matching engine to attempt to find a matching campaign.
    """
    beta = Beta(prompt=prompt)
    result = await CHADX.match(beta)
    return result
