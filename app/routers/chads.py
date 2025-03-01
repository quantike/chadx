import uuid

from fastapi import APIRouter
from loguru import logger
from pydantic import UUID4, BaseModel

from app.dependencies import CHADX, Chad

router = APIRouter(
    prefix="/chads",
    tags=["chads"],
    responses={404: {"description":  "not found"}}
)

# TODO: Store the UUIDs somewhere
@router.post("/signup")
async def post_login():
    return uuid.uuid4()


class CampaignPayload(BaseModel):
    id: str
    chad: Chad


class CampaignResponse(BaseModel):
    campaign_id: UUID4



# TODO: Check that the ID exists somehere
@router.post("/campaign")
async def post_campaign(payload: CampaignPayload) -> CampaignResponse:
    # Append a new advertisement
    CHADX.chads.append(payload.chad)
    logger.info(f"insert chad: {payload.id}")

    return CampaignResponse(campaign_id=uuid.uuid4())

@router.get("/campaign/{id}")
async def get_campaign(id: uuid.UUID) -> uuid.UUID:
    pass
