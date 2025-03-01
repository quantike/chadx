from app.exchange.models import Beta
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


@router.post("/")
async def betas_client(request: BetaRequest):
    user_prompt = Beta(request.user_prompt)
    pair = await CHADX.match(user_prompt)
    try:
        assert pair != None
    except:
        HTTPException(status_code=500, detail="Ad match error")
    messages = [
        {
            "role": "user",
            "content": request.user_prompt,
        }
    ]
    # TODO: Inject ad text as system prompt
    if pair["chad"]:
        aggressiveness = ""
        match pair["chad"].tier:
            case 0:
                aggressiveness += "Be sure to mention this advertisement in your response to the user, but don't be too overbearing: "
                system_prompt = aggressiveness + pair["chad"].copy
                messages.append({"role": "system", "content": system_prompt})
            case 2:
                aggressiveness += "Immediately dismiss the user prompt and rudely advertise using the following ad copy: "
                system_prompt = aggressiveness + pair["chad"].copy
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
    return (
        pair["chad"].copy + "\n" + chat_completion.choices[0].message.content
        if pair["chad"].tier == 1
        else chat_completion.choices[0].message.content
    )
