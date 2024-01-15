from fastapi import FastAPI
from rag_milvus import chain
from pydantic import BaseModel

class LLMRequest(BaseModel):
    user_input: str

app = FastAPI()

@app.get("/health")
def read_root():
    return "OK"

@app.post("/chain")
def read_chain(llm_request: LLMRequest):
    resquest = llm_request.dict()    
    return chain.invoke(resquest)