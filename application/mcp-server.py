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

from datetime import datetime, timedelta
import pandas as pd
def get_cost_analysis(days: str=30):
    """Cost analysis data collection"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # cost explorer
        ce = boto3.client('ce')

        # service cost
        service_response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )
        
        service_costs = pd.DataFrame([
            {
                'SERVICE': group['Keys'][0],
                'cost': float(group['Metrics']['UnblendedCost']['Amount'])
            }
            for group in service_response['ResultsByTime'][0]['Groups']
        ])
        
        # region cost
        region_response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'REGION'}]
        )
        # logger.info(f"Region Cost: {region_response}")
        
        region_costs = pd.DataFrame([
            {
                'REGION': group['Keys'][0],
                'cost': float(group['Metrics']['UnblendedCost']['Amount'])
            }
            for group in region_response['ResultsByTime'][0]['Groups']
        ])
        
        # Daily Cost
        daily_response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            Granularity='DAILY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )
        
        daily_costs = []
        for time_period in daily_response['ResultsByTime']:
            date = time_period['TimePeriod']['Start']
            for group in time_period['Groups']:
                daily_costs.append({
                    'date': date,
                    'SERVICE': group['Keys'][0],
                    'cost': float(group['Metrics']['UnblendedCost']['Amount'])
                })
        
        daily_costs_df = pd.DataFrame(daily_costs)
        
        return {
            'service_costs': service_costs,
            'region_costs': region_costs,
            'daily_costs': daily_costs_df
        }
        
    except Exception as e:
        print(f"Error in cost analysis: {str(e)}")
        return None

@mcp.tool()
def aws_cost_loader(days: int=30) -> list:
    """
    load aws cost data
    days: the number of days looking for cost data
    return: cost data during days
    """

    return get_cost_analysis(days=days)

from langchain_experimental.tools import PythonAstREPLTool
repl = PythonAstREPLTool()
@mcp.tool()
def repl_coder(code):
    """
    Use this to execute python code and do math. 
    If you want to see the output of a value, you should print it out with `print(...)`. This is visible to the user.
    code: the Python code was written in English
    """
    try:
        result = repl.run(code)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    
    if result is None:
        result = "It didn't return anything."

    return result

if __name__ =="__main__":
    print(f"###### main ######")
    mcp.run(transport="stdio")


