# AWS MCP Servers

여기에서는 AWS MCP 서버들에 대한 정보를 정리합니다.

```java
{
   "mcpServers":{
      "awslabs.core-mcp-server":{
         "command":"uvx",
         "args":[
            "awslabs.core-mcp-server@latest"
         ],
         "env":{
            "FASTMCP_LOG_LEVEL":"ERROR",
            "MCP_SETTINGS_PATH":"path to your mcp server settings"
         }
      },
      "awslabs.bedrock-kb-retrieval-mcp-server":{
         "command":"uvx",
         "args":[
            "awslabs.bedrock-kb-retrieval-mcp-server@latest"
         ],
         "env":{
            "AWS_PROFILE":"default",
            "AWS_REGION":"us-west-2"
         }
      },
      "awslabs.cdk-mcp-server":{
         "command":"uvx",
         "args":[
            "awslabs.cdk-mcp-server@latest"
         ],
         "env":{
            "FASTMCP_LOG_LEVEL":"ERROR"
         }
      },
      "awslabs.cost-analysis-mcp-server":{
         "command":"uvx",
         "args":[
            "awslabs.cost-analysis-mcp-server@latest"
         ],
         "env":{
            "AWS_PROFILE":"default",
            "FASTMCP_LOG_LEVEL":"ERROR"
         }
      },
      "awslabs.nova-canvas-mcp-server":{
         "command":"uvx",
         "args":[
            "awslabs.nova-canvas-mcp-server@latest"
         ],
         "env":{
            "AWS_PROFILE":"default",
            "AWS_REGION":"us-west-2"
         }
      }
   }
}
```

[AWS Knowledge Base Retrieval MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/aws-kb-retrieval-server)

```java
{
  "mcpServers": {
    "aws-kb-retrieval": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-aws-kb-retrieval"
      ],
      "env": {
        "AWS_ACCESS_KEY_ID": "YOUR_ACCESS_KEY_HERE",
        "AWS_SECRET_ACCESS_KEY": "YOUR_SECRET_ACCESS_KEY_HERE",
        "AWS_REGION": "YOUR_AWS_REGION_HERE"
      }
    }
  }
}
```
