import gradio as gr
import pandas as pd


def get_data():
    # Read the CSV file from disk. Replace 'data.csv' with the correct file path.
    df = pd.read_csv("~/Coding/Quantike/chadx/matches.csv")
    
    # Convert the 'timestamp' column to datetime.
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Return the full DataFrame with all columns:
    # chad_id, similarity, matched, timestamp, etc.
    return df

with gr.Blocks() as demo:
    gr.Markdown("# 📈 Real-Time Matching Engine Data")
    with gr.Row():
        with gr.Column():
            # Display the raw data table. This shows every timestamp with the id, similarity, and match status.
            gr.DataFrame(get_data, every=gr.Timer(5))
        with gr.Column():
            # Display a line plot of the similarity over time.
            # Here, the x-axis is the timestamp and the y-axis is similarity.
            # If your Gradio LinePlot supports grouping (e.g. by color), you can specify color="chad_id"
            gr.LinePlot(
                get_data,
                every=gr.Timer(5),
                x="timestamp",
                y="similarity",
                color="chad_id",  # This groups data points by campaign ID if supported
                y_title="Similarity",
                overlay_point=True,
                width=500,
                height=500
            )

demo.queue().launch()  # Run the demo with queuing enabled

