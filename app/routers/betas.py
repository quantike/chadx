from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from groq import AsyncGroq
from loguru import logger
from pydantic import BaseModel

from app.dependencies import CHADX
from app.exchange.models import Beta

load_dotenv()

router = APIRouter(
    prefix="/betas", tags=["betas"], responses={404: {"description": "not found"}}
)


async def generate_response(beta: Beta):
    pair = await CHADX.match(beta)
    logger.info(pair)

    if pair is None:
        raise HTTPException(status_code=500, detail="Ad match error")

    # Build messages list starting with the user's prompt.
    messages = [
        {
            "role": "user",
            "content": beta.prompt,
        }
    ]

    # If a campaign ad is present, inject the appropriate system prompt.
    if pair.get("chad"):
        aggressiveness = ""
        match pair["chad"].tier:
            case 0:
                aggressiveness += (
                    "Be sure to mention this advertisement in your response to the user, "
                    "but don't be too overbearing: "
                )
                system_prompt = aggressiveness + pair["chad"].copy
                messages.append({"role": "system", "content": system_prompt})
            case 2:
                aggressiveness += (
                    "Immediately dismiss the user prompt and rudely advertise using the following ad copy: "
                )
                system_prompt = aggressiveness + pair["chad"].copy
                messages.append({"role": "system", "content": system_prompt})
            # For tier 1, no system prompt is injected at this stage.
    
    # Call Groq with the constructed messages.
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
    logger.info("completed chat w groq routing")

    # If there is a tier 1 ad, prepend its copy to the generated response.
    if pair.get("chad") and pair["chad"].tier == 1:
        return pair["chad"].copy + "\n" + chat_completion.choices[0].message.content
    else:
        return chat_completion.choices[0].message.content


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
