from app.exchange.models import Beta, Chad
from app.dependencies import CHADX
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix="/betas", tags=["betas"], responses={404: {"description": "not found"}}
)


class BetaRequest(BaseModel):
    user_prompt: str


test_chad = Chad(
    id="id",
    tier=1,
    copy="We have half price deals on Joey Kangaroos!",
    budget=100,
    threshold=0.5,
)


@router.post("/")
async def betas_client(request: BetaRequest):
    # TODO: Look for available ads in ads dict
    user_prompt = Beta(request.user_prompt)
    CHADX.chads.append(test_chad)
    match = await CHADX.match(user_prompt)
    try:
        assert match != None
    except:
        HTTPException(status_code=500, detail="Ad match error")

    messages = [
        {
            "role": "user",
            "content": request.user_prompt,
        }
    ]
    # TODO: Inject ad text as system prompt
    if match["system_prompt"]:
        system_prompt = (
            "Be SURE to work the following advertisement into your response: "
            + match["system_prompt"]
        )
        messages.append({"role": "system", "content": system_prompt})

    client = AsyncGroq()
    chat_completion = await client.chat.completions.create(
        messages=messages,  # pyright: ignore
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        max_completion_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )
    return chat_completion.choices[0].message.content
