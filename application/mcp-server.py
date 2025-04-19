import json
import boto3
import traceback
import logging
import sys
import mcp_log as log
import mcp_cost as cost
import mcp_rag as rag
import mcp_s3 as storage
import mcp_nova_canvas as canvas

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
    return await log.list_groups(prefix=prefix, region=region)

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

    return await log.get_logs(
        logGroupName=logGroupName,
        logStreamName=logStreamName,
        startTime=startTime,
        endTime=endTime,
        filterPattern=filterPattern,
        region=region
    )

from typing import List, Optional
from mcp.types import Resource

######################################
# AWS S3
######################################
@mcp.tool()
async def list_buckets(
    start_after: Optional[str] = None,
    max_buckets: Optional[int] = 10,
    region: Optional[str] = "us-west-2"
) -> List[dict]:
    """
    List S3 buckets using async client with pagination
    """
    return await storage.list_buckets(start_after, max_buckets, region)
    
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
    return await storage.list_objects(bucket_name, prefix, max_keys, region)

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
    return await storage.list_resources(start_after, max_buckets, region)


from mcp.server.fastmcp import Context, FastMCP
from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from nova_canvas.consts import (
    DEFAULT_CFG_SCALE,
    DEFAULT_HEIGHT,
    DEFAULT_NUMBER_OF_IMAGES,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_QUALITY,
    DEFAULT_WIDTH,
    NOVA_CANVAS_MODEL_ID,
)

@mcp.tool(name='generate_image')
async def mcp_generate_image(
    ctx: Context,
    prompt: str = Field(
        description='The text description of the image to generate (1-1024 characters)'
    ),
    negative_prompt: Optional[str] = Field(
        default=None,
        description='Text to define what not to include in the image (1-1024 characters)',
    ),
    filename: Optional[str] = Field(
        default=None,
        description='The name of the file to save the image to (without extension)',
    ),
    width: int = Field(
        default=DEFAULT_WIDTH,
        description='The width of the generated image (320-4096, divisible by 16)',
    ),
    height: int = Field(
        default=DEFAULT_HEIGHT,
        description='The height of the generated image (320-4096, divisible by 16)',
    ),
    quality: str = Field(
        default=DEFAULT_QUALITY,
        description='The quality of the generated image ("standard" or "premium")',
    ),
    cfg_scale: float = Field(
        default=DEFAULT_CFG_SCALE,
        description='How strongly the image adheres to the prompt (1.1-10.0)',
    ),
    seed: Optional[int] = Field(default=None, description='Seed for generation (0-858,993,459)'),
    number_of_images: int = Field(
        default=DEFAULT_NUMBER_OF_IMAGES,
        description='The number of images to generate (1-5)',
    ),
    workspace_dir: Optional[str] = Field(
        default=None,
        description="""The current workspace directory where the image should be saved.
        CRITICAL: Assistant must always provide the current IDE workspace directory parameter to save images to the user's current project.""",
    )):
    """Generate an image using Amazon Nova Canvas with text prompt.

    This tool uses Amazon Nova Canvas to generate images based on a text prompt.
    The generated image will be saved to a file and the path will be returned.

    IMPORTANT FOR ASSISTANT: Always send the current workspace directory when calling this tool!
    The workspace_dir parameter should be set to the directory where the user is currently working
    so that images are saved to a location accessible to the user.

    ## Prompt Best Practices

    An effective prompt often includes short descriptions of:
    1. The subject
    2. The environment
    3. (optional) The position or pose of the subject
    4. (optional) Lighting description
    5. (optional) Camera position/framing
    6. (optional) The visual style or medium ("photo", "illustration", "painting", etc.)

    Do not use negation words like "no", "not", "without" in your prompt. Instead, use the
    negative_prompt parameter to specify what you don't want in the image.

    You should always include "people, anatomy, hands, low quality, low resolution, low detail" in your negative_prompt

    ## Example Prompts

    - "realistic editorial photo of female teacher standing at a blackboard with a warm smile"
    - "whimsical and ethereal soft-shaded story illustration: A woman in a large hat stands at the ship's railing looking out across the ocean"
    - "drone view of a dark river winding through a stark Iceland landscape, cinematic quality"

    Returns:
        McpImageGenerationResponse: A response containing the generated image paths.
    """

    return await canvas.mcp_generate_image(ctx, prompt, negative_prompt, filename, width, height, quality, cfg_scale, seed, number_of_images, workspace_dir)

@mcp.tool(name='generate_image_with_colors')
async def mcp_generate_image_with_colors(
    ctx: Context,
    prompt: str = Field(
        description='The text description of the image to generate (1-1024 characters)'
    ),
    colors: List[str] = Field(
        description='List of up to 10 hexadecimal color values (e.g., "#FF9800")'
    ),
    negative_prompt: Optional[str] = Field(
        default=None,
        description='Text to define what not to include in the image (1-1024 characters)',
    ),
    filename: Optional[str] = Field(
        default=None,
        description='The name of the file to save the image to (without extension)',
    ),
    width: int = Field(
        default=1024,
        description='The width of the generated image (320-4096, divisible by 16)',
    ),
    height: int = Field(
        default=1024,
        description='The height of the generated image (320-4096, divisible by 16)',
    ),
    quality: str = Field(
        default='standard',
        description='The quality of the generated image ("standard" or "premium")',
    ),
    cfg_scale: float = Field(
        default=6.5,
        description='How strongly the image adheres to the prompt (1.1-10.0)',
    ),
    seed: Optional[int] = Field(default=None, description='Seed for generation (0-858,993,459)'),
    number_of_images: int = Field(default=1, description='The number of images to generate (1-5)'),
    workspace_dir: Optional[str] = Field(
        default=None,
        description="The current workspace directory where the image should be saved. CRITICAL: Assistant must always provide this parameter to save images to the user's current project.",
    )):
    """Generate an image using Amazon Nova Canvas with color guidance.

    This tool uses Amazon Nova Canvas to generate images based on a text prompt and color palette.
    The generated image will be saved to a file and the path will be returned.

    IMPORTANT FOR Assistant: Always send the current workspace directory when calling this tool!
    The workspace_dir parameter should be set to the directory where the user is currently working
    so that images are saved to a location accessible to the user.

    ## Prompt Best Practices

    An effective prompt often includes short descriptions of:
    1. The subject
    2. The environment
    3. (optional) The position or pose of the subject
    4. (optional) Lighting description
    5. (optional) Camera position/framing
    6. (optional) The visual style or medium ("photo", "illustration", "painting", etc.)

    Do not use negation words like "no", "not", "without" in your prompt. Instead, use the
    negative_prompt parameter to specify what you don't want in the image.

    ## Example Colors

    - ["#FF5733", "#33FF57", "#3357FF"] - A vibrant color scheme with red, green, and blue
    - ["#000000", "#FFFFFF"] - A high contrast black and white scheme
    - ["#FFD700", "#B87333"] - A gold and bronze color scheme

    Returns:
        McpImageGenerationResponse: A response containing the generated image paths.
    """

    return await canvas.mcp_generate_image_with_colors(ctx, prompt, colors, negative_prompt, filename, width, height, quality, cfg_scale, seed, number_of_images, workspace_dir)

    
######################################
# AWS Logs
######################################

if __name__ =="__main__":
    print(f"###### main ######")
    mcp.run(transport="stdio")


