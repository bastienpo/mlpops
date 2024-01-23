"""
Prompt generation for RAG model with Langchain
"""

llama_prompt_template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
