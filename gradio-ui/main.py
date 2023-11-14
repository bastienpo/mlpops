import gradio as gr
import time

def response(message, history):
    # Call API
    return "Hello world!"

demo = gr.ChatInterface(
    response,
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="What is 2 + 2 ?", container=False, scale=7),
    title="Mlpops chatbot",
    examples=["Hello", "Am I cool?", "Are tomatoes vegetables?"],
    cache_examples=True,
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
)

demo.launch(share=True, server_name="0.0.0.0", server_port=7860)
