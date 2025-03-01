from fastapi import APIRouter

router = APIRouter(
    prefix="/chadvertisers",
    tags=["chadvertisers"],
    responses={404: {"description":  "not found"}}
)

fake_chads_db = {}
