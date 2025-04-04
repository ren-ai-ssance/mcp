# MCP Servers

## ArXiv MCP Server

[ArXiv MCP Server](https://github.com/blazickjp/arxiv-mcp-server)는 [Smithery-arxiv-mcp-server](https://smithery.ai/server/arxiv-mcp-server)에 접속해서 아래와 같은 configuration 가져옵니다.

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

![noname](https://github.com/user-attachments/assets/a5b156ec-3dda-40d6-925a-608b12b65448)


## Airbnb

[mcp-server-airbnb](https://github.com/openbnb-org/mcp-server-airbnb)와 [Smithery - Airbnb](https://smithery.ai/server/@openbnb-org/mcp-server-airbnb)에서 config를 가져옵니다. 

```java
{
  "mcpServers": {
    "airbnb": {
      "command": "npx",
      "args": [
        "-y",
        "@openbnb/mcp-server-airbnb",
        "--ignore-robots-txt"
      ]
    }
  }
}
```

이때의 결과는 아래와 같습니다. 


![image](https://github.com/user-attachments/assets/cde0b053-e699-4b65-8e7c-03eea8f8f9ec)
