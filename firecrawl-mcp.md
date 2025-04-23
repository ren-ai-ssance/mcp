# Firecrawl MCP의 활용

[firecrawl](https://www.firecrawl.dev/signin)에 접속하여 API Key를 발급 받습니다. 아래와 같이 MCP config 파일을 준비합니다.

```python
{
  "mcpServers": {
    "firecrawl-mcp": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "API Key"
      }
    }
  }
}
```
