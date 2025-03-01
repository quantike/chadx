from fastapi import APIRouter

router = APIRouter(
    prefix="/chadvertisers",
    tags=["chadvertisers"],
    responses={404: {"description":  "not found"}}
)


@router.post("/campaign")
async def post_campaign(req: ):
