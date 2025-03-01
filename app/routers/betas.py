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


async def generate_response(beta: Beta):
    pair = await CHADX.match(beta)
    try:
        assert pair != None
    except:
        HTTPException(status_code=500, detail="Ad match error")
    messages = [
        {
            "role": "user",
            "content": beta.prompt,
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


class BetaRequest(BaseModel):
    user_prompt: str


@router.post("/")
async def betas_client(request: BetaRequest):
    beta = Beta(request.user_prompt)
    response = await generate_response(beta)
    return response


class GenerateRequest(BaseModel):
    id: str
    n_betas: int


@router.post("/generate")
async def generate_betas(request: GenerateRequest):
    """Create synthetic user prompts based on the target ad copy"""
    chad_or_none = await CHADX.get(request.id)
    if not chad_or_none:
        return HTTPException(status_code=404, detail="No chad campaign found")

    client = AsyncGroq()
    messages = [
        {
            "role": "user",
            "content": "Generate a user question that is vaguely related to the following ad copy: "
            + chad_or_none.copy,
        }
    ]

    completions = []
    for _ in range(request.n_betas):
        chat_completion = await client.chat.completions.create(
            messages=messages,  # pyright: ignore
            model="llama-3.3-70b-versatile",
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )
        completions.append(chat_completion.choices[0].message.content)

    responses = []
    for user_prompt in completions:
        beta = Beta(user_prompt)
        response = await generate_response(beta)
        responses.append(response)
    return responses
