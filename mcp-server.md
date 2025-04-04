# MCP Servers

## ArXiv MCP Server

[ArXiv MCP Server](https://github.com/blazickjp/arxiv-mcp-server)는 [Smithery-arxiv-mcp-server]에 접속해서 아래와 같은 configuration 가져옵니다.

```java
{
  "mcpServers": {
    "arxiv-mcp-server": {
      "command": "npx",
      "args": [
        "-y",
        "@smithery/cli@latest",
        "run",
        "arxiv-mcp-server",
        "--config",
        "{\"storagePath\":\"/Users/ksdyb/Downloads/ArXiv\"}"
      ]
    }
  }
}
```

[ArXiv.md](./ArXiv.md)와 같이 설정후 실행한 결과는 아래와 같습니다. 논문 데이터를 근거로 아래와 같은 결과를 얻을 수 있습니다.

![noname](https://github.com/user-attachments/assets/ce4fd9ab-037f-4d6d-8afa-93a3bef9f238)
