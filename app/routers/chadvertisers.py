import uuid

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/chadvertisers",
    tags=["chadvertisers"],
    responses={404: {"description":  "not found"}}
)

# TODO: Store the UUIDs somewhere
@router.post("/signup")
async def post_login():
    return uuid.uuid4()


class CampaignPayload(BaseModel):
    id: str
    prompt: str


# TODO: Check that the ID exists somehere
@router.post("/campaign")
async def post_campaign(payload: CampaignPayload):
    return payload.prompt
