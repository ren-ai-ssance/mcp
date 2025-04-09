import json
import boto3
import traceback
import logging
import sys
import mcp_log as log
import mcp_cost as cost
import mcp_rag as rag

from typing import Dict, Optional, Any
from langchain_experimental.tools import PythonAstREPLTool
from mcp.server.fastmcp import FastMCP 

logging.basicConfig(
    level=logging.INFO,  # Default to INFO level
    format='%(filename)s:%(lineno)d | %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger("mcp-server")

try:
    mcp = FastMCP(
        name = "Search",
        instructions=(
            "You are a helpful assistant. "
            "You can search the documentation for the user's question and provide the answer."
        ),
    )
    logger.info("MCP server initialized successfully")
except Exception as e:
        err_msg = f"Error: {str(e)}"
        logger.info(f"{err_msg}")

######################################
# RAG
######################################
@mcp.tool()
def search(keyword: str) -> str:
    "search keyword"

    return rag.retrieve_knowledge_base(keyword)

######################################
# Code Interpreter
######################################
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

######################################
# AWS Cost
######################################
@mcp.tool()
def aws_cost_loader(days: int=30, region: str='us-west-2') -> list:
    """
    load aws cost data
    days: the number of days looking for cost data
    region: the name of aws region
    return: cost data during days
    """

    return cost.get_cost_analysis(days=days, region=region)

######################################
# AWS Logs
######################################
@mcp.tool()
async def list_groups(
    prefix: Optional[str] = None,
    region: Optional[str] = 'us-west-2'
) -> str:
    """List available CloudWatch log groups."""
    return log.list_groups(prefix=prefix, region=region)

@mcp.tool()
async def get_logs(
    logGroupName: str,
    logStreamName: Optional[str] = None,
    startTime: Optional[str] = None,
    endTime: Optional[str] = None,
    filterPattern: Optional[str] = None,
    region: Optional[str] = 'us-west-2'
) -> str:
    """Get CloudWatch logs from a specific log group and stream."""

    return log.get_logs(
        logGroupName=logGroupName,
        logStreamName=logStreamName,
        startTime=startTime,
        endTime=endTime,
        filterPattern=filterPattern,
        region=region
    )

import asyncio
import os
from typing import List, Optional, Dict
from mcp.types import Resource
import aioboto3

session = aioboto3.Session()

@mcp.tool()
async def list_buckets(
    start_after: Optional[str] = None,
    max_buckets: Optional[int] = 5,
    region: Optional[str] = "us-west-2"
) -> List[dict]:
    """
    List S3 buckets using async client with pagination
    """
    async with session.client('s3', region_name=region) as s3:
        if configured_buckets:
            # If buckets are configured, only return those
            response = await s3.list_buckets()
            all_buckets = response.get('Buckets', [])
            configured_bucket_list = [
                bucket for bucket in all_buckets
                if bucket['Name'] in configured_buckets
            ]

            #
            if start_after:
                configured_bucket_list = [
                    b for b in configured_bucket_list
                    if b['Name'] > start_after
                ]

            return configured_bucket_list[:max_buckets]
        else:
            # Default behavior if no buckets configured
            response = await s3.list_buckets()
            buckets = response.get('Buckets', [])

            if start_after:
                buckets = [b for b in buckets if b['Name'] > start_after]

            return buckets[:max_buckets]

def _get_configured_buckets() -> List[str]:
    """
    Get configured bucket names from environment variables.
    Format in .env file:
    S3_BUCKETS=bucket1,bucket2,bucket3
    or
    S3_BUCKET_1=bucket1
    S3_BUCKET_2=bucket2
    see env.example ############
    """
    # Try comma-separated list first
    bucket_list = os.getenv('S3_BUCKETS')
    if bucket_list:
        return [b.strip() for b in bucket_list.split(',')]

    buckets = []
    i = 1
    while True:
        bucket = os.getenv(f'S3_BUCKET_{i}')
        if not bucket:
            break
        buckets.append(bucket.strip())
        i += 1

    return buckets            

configured_buckets = _get_configured_buckets()

@mcp.tool()  
async def list_objects(
    bucket_name: str, 
    prefix: Optional[str] = "", 
    max_keys: Optional[int] = 1000,
    region: Optional[str] = "us-west-2"
) -> List[dict]:
    """
    List objects in a specific bucket using async client with pagination
    Args:
        bucket_name: Name of the S3 bucket
        prefix: Object prefix for filtering
        max_keys: Maximum number of keys to return,
        region: Name of the aws region
    """
    #
    if configured_buckets and bucket_name not in configured_buckets:
        logger.warning(f"Bucket {bucket_name} not in configured bucket list")
        return []

    async with session.client('s3', region_name=region) as s3:
        response = await s3.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix,
            MaxKeys=max_keys
        )
        return response.get('Contents', [])

def is_text_file(key: str) -> bool:
    """Determine if a file is text-based by its extension"""
    text_extensions = {
        '.txt', '.log', '.json', '.xml', '.yml', '.yaml', '.md',
        '.csv', '.ini', '.conf', '.py', '.js', '.html', '.css',
        '.sh', '.bash', '.cfg', '.properties'
    }
    return any(key.lower().endswith(ext) for ext in text_extensions)
    
@mcp.tool()    
async def list_resources(
    start_after: Optional[str] = None,
    max_buckets: Optional[int] = 10,
    region: Optional[str] = "us-west-2"
) -> List[Resource]:
    """
    List S3 buckets and their contents as resources with pagination
    Args:
        start_after: Start listing after this bucket name
    """
    resources = []
    logger.debug("Starting to list resources")
    
    logger.debug(f"Configured buckets: {configured_buckets}")

    try:
        # Get limited number of buckets
        buckets = await list_buckets(start_after, max_buckets, region)
        logger.debug(f"Processing {len(buckets)} buckets (max: {max_buckets})")

        # # limit concurrent operations
        # async def process_bucket(bucket):
        #     bucket_name = bucket['Name']
        #     logger.debug(f"Processing bucket: {bucket_name}")

        #     try:
        #         # List objects in the bucket with a reasonable limit
        #         objects = await list_objects(bucket_name, max_keys=1000)

        #         for obj in objects:
        #             if 'Key' in obj and not obj['Key'].endswith('/'):
        #                 object_key = obj['Key']
        #                 mime_type = "text/plain" if is_text_file(object_key) else "text/markdown"

        #                 resource = Resource(
        #                     uri=f"s3://{bucket_name}/{object_key}",
        #                     name=object_key,
        #                     mimeType=mime_type
        #                 )
        #                 resources.append(resource)
        #                 logger.debug(f"Added resource: {resource.uri}")

        #     except Exception as e:
        #         logger.error(f"Error listing objects in bucket {bucket_name}: {str(e)}")

        # Use semaphore to limit concurrent bucket processing
        # semaphore = asyncio.Semaphore(3)  # Limit concurrent bucket processing
        # async def process_bucket_with_semaphore(bucket):
        #     async with semaphore:
        #         await process_bucket(bucket)

        # Process buckets concurrently
        # await asyncio.gather(*[process_bucket_with_semaphore(bucket) for bucket in buckets])

    except Exception as e:
        logger.error(f"Error listing buckets: {str(e)}")
        raise

    logger.info(f"Returning {len(resources)} resources")
    return resources

######################################
# AWS Logs
######################################

if __name__ =="__main__":
    print(f"###### main ######")
    mcp.run(transport="stdio")


