import json
import boto3
import re
import traceback

from botocore.config import Config
from langchain_aws import BedrockEmbeddings
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from pydantic.v1 import BaseModel, Field
from multiprocessing import Process, Pipe

def load_config():
    config = None
    try:
        with open("/home/config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            print(f"config: {config}")

    except Exception:
        print("use local configuration")
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
    
    return config

config = load_config()

projectName = config["projectName"] if "projectName" in config else "langgraph-nova"
index_name = projectName


from mcp.server.fastmcp import FastMCP 

mcp = FastMCP("Math") 

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    return a * b

projectName = "mcp-rag"
knowledge_base_name = projectName
@mcp.tool()
def get_answer(query: str) -> str:
    "answer to the general question"
    return get_answer_using_opensearch(query)

if __name__ =="__main__":
    print(f"###### main ######")
    mcp.run(transport="stdio")

