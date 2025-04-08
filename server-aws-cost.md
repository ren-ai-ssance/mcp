# AWS Cost Anaysis MCP Server


pip install uvx


[Cost Analysis MCP Server](https://awslabs.github.io/mcp/servers/cost-analysis-mcp-server/)에 따라 MCP server를 설정하면 아래와 같습니다.

```java
{
  "mcpServers": {
    "awslabs.cost-analysis-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.cost-analysis-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR",
        "AWS_PROFILE": "default"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

Tool에 대한 정보는 잘 가져오나 전혀 동작이 안됩니다.

![image](https://github.com/user-attachments/assets/143c7728-38c0-4917-8d10-3c1fd1157b34)
