from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import os
import boto3


ssm = boto3.client("ssm", region_name="ap-southeast-2")

param = ssm.get_parameter(
    Name="OpenAI-API-1",
    WithDecryption=True
)

api_key = param["Parameter"]["Value"]


app = FastAPI()
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.environ["OPENAI_API_KEY"]
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
