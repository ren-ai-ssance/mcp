# MCP Nova Canvas

[Amazon Nova Canvas MCP Server](https://awslabs.github.io/mcp/servers/nova-canvas-mcp-server/)와 같이 MCP를 이용해 Amazon Nova Canvas로 그림을 생성할 수 있습니다.

```java
{
  "mcpServers": {
    "awslabs.nova-canvas-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.nova-canvas-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "your-aws-profile",
        "AWS_REGION": "us-east-1",
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

[mcp_server_image_generation.py]에서는 [Amazon Nova Canvas MCP Server](https://awslabs.github.io/mcp/servers/nova-canvas-mcp-server/)를 Cloud 환경에서 실행할 수 있도록 일부 설정을 변경하였습니다. 

이때의 결과는 아래와 같습니다.

![image](https://github.com/user-attachments/assets/179cd1be-e658-40fe-a2bc-67d3b95270b6)

