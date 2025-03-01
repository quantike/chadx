import gradio as gr
from exchange.models import Beta
from routers.betas import generate_response


def message_with_ads(messages: str, history):
    beta = Beta(prompt=messages)
    return await generate_response(beta)


gr.ChatInterface(
    fn=message_with_ads,
    type="messages",
    title="chadx",
    description="free access to SOTA models",
    # theme="ocean",
    examples=["How can I win my Hackathon?", "What is an agent?", "What the hell is attention?"],
    # cache_examples=True,
).launch()

gr.ChatInterface
