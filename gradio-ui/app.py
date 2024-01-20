import gradio as gr
import requests

def response(message, history):    
    res = requests.post(
        "http://localhost:9042/chain", 
        json={
            "user_input": message, 
        }
    )

    return res.json()

demo = gr.ChatInterface(
    response,
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="What is 2 + 2 ?", container=False, scale=7),
    title="Mlpops chatbot",
    examples=["Hello", "Am I cool?", "Are tomatoes vegetables?"],
    cache_examples=False,
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
)

if __name__ == "__main__":
    demo.queue().launch(server_name="0.0.0.0", server_port=7860)
