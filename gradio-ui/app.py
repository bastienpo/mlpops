import gradio as gr
import requests

def response(message, history):    
    res = requests.post(
        "http://localhost:9042/chain", 
        json={
            "question": message, 
        }
    )

    return res.json()

demo = gr.ChatInterface(
    response,
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="On what data has the model been trained ?", container=False, scale=7),
    title="Mlpops RAG Chatbot",
    examples=["What BLEU score does the model achieve?", "What is the composition of the encoder?", "On what data has the model been trained?"],
    cache_examples=False,
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
)

if __name__ == "__main__":
    demo.queue().launch(server_name="0.0.0.0", server_port=7860)
