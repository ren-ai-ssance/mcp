# AWS CLI MCP

AWS CLI를 위한 tool을 아래와 같이 정의합니다. 

```python
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
```

이를 활용하면 아래와 같은 결과를 얻을 수 있습니다.

![image](https://github.com/user-attachments/assets/16a248aa-9244-436a-a090-4b6edb891d4e)
