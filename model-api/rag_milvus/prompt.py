"""
Prompt generation for RAG model with Langchain
"""

llama_prompt_template = """
<s>[INST] <<SYS>>
{context}
<</SYS>>

{message} [/INST]
"""