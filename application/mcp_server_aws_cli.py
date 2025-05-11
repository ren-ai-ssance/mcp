import logging
import sys
import mcp_basic
import subprocess

from mcp.server.fastmcp import FastMCP 

logging.basicConfig(
    level=logging.INFO,  # Default to INFO level
    format='%(filename)s:%(lineno)d | %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger("aws-cli")

try:
    mcp = FastMCP(
        name = "tools",
        instructions=(
            "You are a helpful assistant. "
            "You can use tools for the user's question and provide the answer."
        ),
    )
    logger.info("MCP server initialized successfully")
except Exception as e:
        err_msg = f"Error: {str(e)}"
        logger.info(f"{err_msg}")


######################################
# AWS CLI
######################################

@mcp.tool()    
def run_aws_cli(command: str, subcommand: str, options: str) -> str:
    """
    run aws command using aws cli and then return the result
    command: AWS CLI command (e.g., s3, ec2, dynamodb)
    subcommand: subcommand for the AWS CLI command (e.g., ls, cp, get-object)
    options: additional options for the command (e.g., --bucket mybucket)
    return: command output as string
    """   
    logger.info(f"run_aws_cli_ommand --> command: {command}, subcommand: {subcommand}, options: {options}")
    
    # 명령어 구성
    cmd = ['aws', command, subcommand]
    logger.info(f"run_aws_cli_ommand --> cmd: {cmd}")
    
    if options:
        options_list = options.split()
        cmd.extend(options_list)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        error_message = f"execution error: {e.stderr}"
        logger.error(error_message)
        return error_message
    except Exception as e:
        error_message = f"{str(e)}"
        logger.error(error_message)
        return error_message

@mcp.tool()    
def retrieve_aws_cost(start_date: str, end_date: str, granularity: str = "MONTHLY") -> str:
    """
    Retrieve AWS costs using AWS Cost Explorer for the specified period.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        granularity: Data grouping unit (DAILY, MONTHLY, HOURLY)
    
    Returns:
        AWS cost information in JSON format
    """
    logger.info(f"retrieve_aws_cost --> start_date: {start_date}, end_date: {end_date}, granularity: {granularity}")
    
    cmd = [
        'aws', 'ce', 'get-cost-and-usage',
        '--time-period', f'Start={start_date},End={end_date}',
        '--granularity', granularity,
        '--metrics', 'UnblendedCost',
        '--group-by', 'Type=DIMENSION,Key=SERVICE'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        error_message = f"Cost retrieval execution error: {e.stderr}"
        logger.error(error_message)
        return error_message
    except Exception as e:
        error_message = f"{str(e)}"
        logger.error(error_message)
        return error_message

@mcp.tool()    
def list_objects(bucket_name: str, prefix: str = "", delimiter: str = "") -> str:
    """
    List objects in an S3 bucket using list-objects-v2 command.
    
    Args:
        bucket_name: Name of the S3 bucket
        prefix: Optional prefix to filter objects (e.g., 'folder/')
        delimiter: Optional delimiter to group objects (e.g., '/')
    
    Returns:
        List of objects in the bucket in JSON format
    """
    logger.info(f"list_objects --> bucket_name: {bucket_name}, prefix: {prefix}, delimiter: {delimiter}")
    
    cmd = ['aws', 's3api', 'list-objects-v2', '--bucket', bucket_name]
    
    if prefix:
        cmd.extend(['--prefix', prefix])
    if delimiter:
        cmd.extend(['--delimiter', delimiter])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        error_message = f"Failed to list objects: {e.stderr}"
        logger.error(error_message)
        return error_message
    except Exception as e:
        error_message = f"{str(e)}"
        logger.error(error_message)
        return error_message

if __name__ =="__main__":
    print(f"###### main ######")
    mcp.run(transport="stdio")


