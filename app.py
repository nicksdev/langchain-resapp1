from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import os

print (os.getenv("API_KEY"))
api_key = os.getenv("API_KEY")


app = FastAPI()
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.environ["API_KEY"]
)
@app.get("/")
async def root():
    return {"status": "running"}
@app.get("/ask")
async def ask(q: str):
    response = llm.invoke([
        HumanMessage(content=q)
    ])
    return {
        "question": q,
        "answer": response.content
    }
