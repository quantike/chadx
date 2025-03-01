import gradio as gr
import requests


def message_with_ads(message, history):
    """
    Sends the user's message as 'user_prompt' to the FastAPI /betas/ endpoint.
    The endpoint processes the prompt and returns the generated response.
    """
    url = "http://localhost:8000/betas/"  # Update the host/port if needed.
    payload = {"user_prompt": message}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors.
        generated_response = response.json()
    except Exception as e:
        print(f"Error calling FastAPI endpoint: {e}")
        generated_response = "Error generating response."
    
    return generated_response

iface = gr.ChatInterface(
    fn=message_with_ads,
    type="messages",
    title="chadx",
    description="Free access to SOTA models with campaign ad injection",
    examples=[
        "How can I win my Hackathon?",
        "What is an agent?",
        "What the hell is attention?"
    ],
)

iface.launch()
