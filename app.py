from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from fastapi.middleware.cors import CORSMiddleware
import boto3


#from dotenv import load_dotenv
#import os
#load_dotenv()



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create SSM client
ssm = boto3.client("ssm", region_name="ap-southeast-2")

# Fetch API key from Parameter Store
parameter = ssm.get_parameter(
    Name="OpenAI-API-1",  # your parameter name
    WithDecryption=True
)

api_key = parameter["Parameter"]["Value"]


#api_key = os.getenv("API_KEY")



llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=api_key
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
