from fastapi import FastAPI

# from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import chads, betas, embedder

app = FastAPI()

app.include_router(chads.router)
app.include_router(betas.router)
app.include_router(embedder.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    # dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "chadx"}
