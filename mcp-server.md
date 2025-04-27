# MCP Servers

## 활용도 높은 MCP Server들

### ArXiv MCP Server

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


### Airbnb

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


### Obsidian Memo

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

### Playwright MCP

[playwright-mcp](https://github.com/microsoft/playwright-mcp)을 이용하여 웹 페이지와 상호작용할 수 있도록 돕는 구조화된 접근성 스냅샷을 활용합니다. [Playwright MCP Config](https://github.com/microsoft/playwright-mcp?tab=readme-ov-file#example-config)에 접속하여 config를 가져옵니다. 상세한 내용은 [Playwright.md](https://github.com/kyopark2014/mcp/blob/main/Playwright.md)을 참조합니다.

```java
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest"
      ]
    }
  }
}
```

이제 "https://github.com/kyopark2014/technical-summary/blob/main/api-gateway-log.md를 참조하여 로깅에 대한 정보를 정리하세요."와 같이 입력하면, 해당 URL을 열어서 관련정보를 가져온 후에 아래와 같이 답변합니다.

![image](https://github.com/user-attachments/assets/28c9125b-f2bf-4383-ac7a-185ea8c45e6b)

### Filesystem

[Filesystem.md](https://github.com/kyopark2014/mcp/blob/main/Filesystem.md)와 같이 파일 정보를 읽거나 생성할 수 있습니다. 

아래와 같이 config를 설정합니다. 

```java
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
	    "@modelcontextprotocol/server-filesystem",
        "/Users/ksdyb/Documents"
      ]
    }
  }
}
```

이제 "파일의 갯수를 알려주세요."를 입력하고 결과를 확인합니다.

![image](https://github.com/user-attachments/assets/04bb29db-17c8-42c0-a277-927ddfd95249)

"test.txt 파일을 생성하고, 파일에 "안녕하세요."라고 입력하세요."라고 입력하면 파일을 생성할 수 있습니다.

![image](https://github.com/user-attachments/assets/4fe08e44-5535-4769-bccf-763a3dde7109)

### AWS Documents 

AWS의 Document를 조회할 수 있습니다.

```java
{
    "mcpServers": {
	"awslabs.aws-documentation-mcp-server": {
	    "command": "uvx",
	    "args": ["awslabs.aws-documentation-mcp-server@latest"],
	    "env": {
		"FASTMCP_LOG_LEVEL": "ERROR"
	    }
	}
    }
}
```

## Reference

[Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers/blob/main/README-ko.md)

