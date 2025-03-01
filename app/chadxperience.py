import requests
import json
import gradio as gr

# Store previous data points for incremental updates
timestamps = []
impressions = []


def send_chad_request(id, tier, copy, budget, threshold):
    url = "http://127.0.0.1:8000/chads/campaign"
    headers = {"Content-Type": "application/json"}
    payload = {
        "id": id,
        "tier": int(tier),
        "copy": copy,
        "budget": float(budget),
        "threshold": float(threshold),
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.text


def send_generate_request(id):
    url = "http://127.0.0.1:8000/betas/generate"
    headers = {"Content-Type": "application/json"}
    payload = {"id": id, "n_betas": 5}

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.text


def run_sim_and_plot(id):
    """Runs the Beta simulation and updates the graph incrementally."""
    sim_result = send_generate_request(id)  # Run simulation
    return sim_result


with gr.Blocks() as chadxperience:
    gr.Markdown("## Submit Campaign Request")
    with gr.Row():
        id_input = gr.Textbox(label="Campaign ID")
        tier_input = gr.Number(label="Aggression Tier", value=2)
    copy_input = gr.Textbox(label="Ad Copy", lines=3)
    budget_input = gr.Number(label="Budget", value=100)
    threshold_input = gr.Number(label="Threshold", value=0.0)
    submit_button = gr.Button("Submit")
    chad_output = gr.Textbox(label="Campaign set for ID:")

    # Beta Sim
    run_beta_sim = gr.Button("Run Sim on Beta Bots")
    sim_output = gr.Textbox(label="Sim Results")

    submit_button.click(
        send_chad_request,
        inputs=[id_input, tier_input, copy_input, budget_input, threshold_input],
        outputs=chad_output,
    )

    run_beta_sim.click(
        run_sim_and_plot,
        inputs=id_input,
        outputs=sim_output,
    )

chadxperience.launch()
