import json
import boto3
import traceback

def load_config():
    config = None
    try:
        with open("application/config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            print(f"config: {config}")
    except Exception:
        err_msg = traceback.format_exc()
        print(f"error message: {err_msg}")    
    return config

config = load_config()

bedrock_region = config["region"] if "region" in config else "us-west-2"
projectName = config["projectName"] if "projectName" in config else "mcp-rag"
accountId = config["accountId"] if "accountId" in config else None
if accountId is None:
    raise Exception ("No accountId")
region = config["region"] if "region" in config else "us-west-2"
print(f"region: {region}")

numberOfDocs = 3
multi_region = "Enable"
model_name = "Claude 3.5 Haiku"
knowledge_base_name = projectName

def retrieve_knowledge_base(query):
    lambda_client = boto3.client(
        service_name='lambda',
        region_name=bedrock_region
    )

    functionName = f"lambda-rag-for-{projectName}"
    print(f"functionName: {functionName}")

    try:
        payload = {
            'function': 'search_rag',
            'knowledge_base_name': knowledge_base_name,
            'keyword': query,
            'top_k': numberOfDocs,
            'grading': "Enable",
            'model_name': model_name,
            'multi_region': multi_region
        }
        print(f"payload: {payload}")

        output = lambda_client.invoke(
            FunctionName=functionName,
            Payload=json.dumps(payload),
        )
        payload = json.load(output['Payload'])
        print(f"response: {payload['response']}")
        
    except Exception:
        err_msg = traceback.format_exc()
        print(f"error message: {err_msg}")       

    return payload['response'], []    

from mcp.server.fastmcp import FastMCP 

mcp = FastMCP(
    name = "Search",
    instructions=(
        "You are a helpful assistant. "
        "You can search the documentation for the user's question and provide the answer."
    ),
) 

@mcp.tool()
def search(keyword: str) -> str:
    "search keyword"

    return retrieve_knowledge_base(keyword)

if __name__ =="__main__":
    print(f"###### main ######")
    mcp.run(transport="stdio")


