"""
Prompt generation for RAG model with Langchain
"""

llama_prompt_template = """
<s>[INST] <<SYS>>
Respond with short answers with factual informations.

{context}
<</SYS>>

{message} [/INST]
"""
