from dotenv import load_dotenv

from fastapi import APIRouter, HTTPException
from groq import AsyncGroq
from loguru import logger
from pydantic import BaseModel

from app.dependencies import CHADX
from app.exchange.models import Beta
from langfuse import Langfuse
from langfuse.decorators import langfuse_context, observe

load_dotenv()

langfuse = Langfuse()

router = APIRouter(
    prefix="/betas", tags=["betas"], responses={404: {"description": "not found"}}
)

MODEL = "llama-3.3-70b-versatile"


@observe(as_type="generation")
async def generate_response(beta: Beta):
    """
    Take a user's prompt and return an LLM response.

    Args:
        beta (Beta): A class that holds a user's prompt. More to come.
    """

    # Add session_id to Langfuse Trace to enable session tracking
    langfuse_context.update_current_observation(
        model=MODEL,
        input=beta.prompt,
    )

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
                aggressiveness += "Immediately dismiss the user prompt and rudely advertise using the following ad copy: "
                system_prompt = aggressiveness + pair["chad"].copy
                messages.append({"role": "system", "content": system_prompt})
            # For tier 1, no system prompt is injected at this stage.

    # Call Groq with the constructed messages.
    client = AsyncGroq()
    chat_completion = await client.chat.completions.create(
        messages=messages,  # pyright: ignore
        model=MODEL,
        temperature=0.5,
        max_completion_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )
    logger.info("completed chat w groq routing")
    response = chat_completion.choices[0].message.content

    # If there is a tier 1 ad, append its copy to the generated response.
    if pair.get("chad") and pair["chad"].tier == 1:
        response = response + "\n" + pair["chad"].copy

    langfuse_context.update_current_observation(
        usage_details={"input": len(beta.prompt), "output": len(response)},
        output=response,
    )

    return response


class BetaRequest(BaseModel):
    user_prompt: str


@router.post("/")
async def betas_client(request: BetaRequest):
    beta = Beta(request.user_prompt)
    response = await generate_response(beta)
    return response
