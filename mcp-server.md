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


## Obsidian Memo

[Obsidian MCP Server](https://github.com/smithery-ai/mcp-obsidian)를 이용하기 위해, [Smithery - Obsidian](https://smithery.ai/server/mcp-obsidian)에서 config를 가져옵니다. 상세한 내용은 [Obsidian.md](./Obsidian.md)을 참조합니다.

```java
{
  "mcpServers": {
    "mcp-obsidian": {
      "command": "npx",
      "args": [
        "-y",
        "@smithery/cli@latest",
        "run",
        "mcp-obsidian",
        "--config",
        "{\"vaultPath\":\"/Users/ksdyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/memo\"}"
      ]
    }
  }
}
```

아래와 같이 "CSAT 풀었던 결과는?"라고 질의하면, 내 컴퓨터의 Obsidian 메모의 내용을 참조하여 답변합니다.

![image](https://github.com/user-attachments/assets/5c83eee1-262d-428e-97d7-fac3d9f38f2a)

