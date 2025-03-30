# Model Context Protocol

MCP(Model Context Protocal)은 Anthropic에서 기여하고 있는 오픈소스 프로젝트입니다. 2024년 11월에 MCP가 이렇게 성공할 것으로 예상한 사람은 많지 않았을것 같습니다. 저는 API 기반의 시스템 인터페이스를 선호했기에 MCP는 그다지 매력적이지 않았습니다. 하지만 이제 MCP는 LLM이 외부 context를 가져오는 방법으로 주된 인터페이스가 되었고 향후 이런 방향은 더 가속화될것 입니다. 

[MCP with LangChain](https://tirendazacademy.medium.com/mcp-with-langchain-cabd6199e0ac)을 참조합니다.

```text
pip install langchain-mcp-adapters
```


### MCP inspector

Development Mode에서 mcp server를 테스트 하기 위해 MCP inspector를 이용할 수 있습니다. 아래와 같이 cli를 설치합니다. 

```text
pip install 'mcp[cli]'
```

이후 아래와 같이 실행하면 쉽게 mcp-server.py의 동작을 테스트 할 수 있습니다. 실행시 http://localhost:5173 와 같은 URL을 제공합니다.

```text
mcp dev mcp-server.py
```

## MCP Servers의 활용

[Model Context Protocol servers](https://github.com/modelcontextprotocol/servers)에서 쓸만한 서버군을 찾아봅니다. 

- [Perplexity Ask MCP Server](https://github.com/ppl-ai/modelcontextprotocol)
- [Riza MCP Server](https://github.com/riza-io/riza-mcp)
- [Tavily MCP Server](https://github.com/tavily-ai/tavily-mcp)



## MCP Server 정보 업데이트

아래와 같이 json 형식의 서버정보를 업데이트 할 수 있습니다. 아래에서는 [mcp-server.py](./application/mcp-server.py)에서 정의한 search를 이용하고 있습니다.

```java
{
  "mcpServers": {
    "search": {
      "command": "python",
      "args": [
        "application/mcp-server.py"
      ]
    }
  }
}
```

## 실행하기

Output의 environmentformcprag의 내용을 복사하여 application/config.json을 생성합니다. "aws configure"로 credential이 설정되어 있어야합니다. 만약 visual studio code 사용자라면 config.json 파일은 아래 명령어를 사용합니다.

```text
code application/config.json
```

아래와 같이 필요한 패키지를 설치합니다.

```text
python3 -m venv venv
source venv/bin/activate
pip install streamlit streamlit_chat 
pip install boto3 langchain_aws langchain langchain_community langgraph opensearch-py
pip install beautifulsoup4 pytz tavily-python
```

아래와 같은 명령어로 streamlit을 실행합니다. 

```text
streamlit run application/app.py
```

## 실행 결과

### MCP로 RAG를 조회하여 활용하기

[error_code.pdf](./contents/error_code.pdf)을 다운로드 한 후에 파일을 업로드합니다. 이후 아래와 같이 "보일러 에러중 수압과 관련된 에러 코드를 검색해주세요."와 같이 입력하면 mcp를 이용해 tool의 정보를 가져오고, search tool로 얻어진 정보를 이용해 아래와 같은 정보를 보여줄 수 있습니다. 이때 search tool은 lambda를 실행하는데 lambda에서는 완전 관리형 RAG 서비스인 knowledge base를 이용하여 검색어를 조회하고 관련성을 평가한 후에 관련된 문서만을 전달합니다. Agent는 RAG를 조회하여 얻어진 정보로 답변을 아래와 같이 구합니다.

<img src="https://github.com/user-attachments/assets/01b5e47f-ada1-405e-8455-3d3ce260cb41" width="700">

### MCP로 인터넷 검색을 하여 활용하기

[smithery-Tavily](https://smithery.ai/server/mcp-tavily)에 접속하여 환경에 맞는 설정값을 얻어옵니다. 아래는 Mac/Linux의 JSON format의 접속 정보입니다.

```java
{
  "mcpServers": {
    "mcp-tavily": {
      "command": "npx",
      "args": [
        "-y",
        "@smithery/cli@latest",
        "run",
        "mcp-tavily",
        "--key",
        "132c5aad-6f2f-4e42-19a1-d0b1fcb75613"
      ]
    }
  }
}
```

이 정보를 아래와 같이 왼쪽 메뉴의 MCP Config에 복사합니다.

<img src="https://github.com/user-attachments/assets/0e054f8e-4356-42e0-a70e-636af8d377c8" width="300">


이후 메뉴에서 "Agent"를 선택후에 아래와 같이 "강남역 맛집은?"라고 입력후 결과를 확인합니다.

<img src="https://github.com/user-attachments/assets/8275bf94-2f46-475d-9eea-02568e70199b" width="700">



## Reference 

[MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

[Using MCP with LangGraph agents](https://www.youtube.com/watch?v=OX89LkTvNKQ)

[MCP From Scratch](https://mirror-feeling-d80.notion.site/MCP-From-Scratch-1b9808527b178040b5baf83a991ed3b2)

[Understanding MCP From Scratch](https://www.youtube.com/watch?v=CDjjaTALI68)

[LangChain MCP Adapters](https://github.com/langchain-ai/langchain-mcp-adapters)


["Vibe Coding" LangGraph apps with llms.txt and MCP](https://www.youtube.com/watch?v=fk2WEVZfheI)

[MCP LLMS-TXT Documentation Server](https://github.com/langchain-ai/mcpdoc)



[MCP - For Server Developers](https://modelcontextprotocol.io/quickstart/server)

[Model Context Protocol (MCP) and Amazon Bedrock](https://community.aws/content/2uFvyCPQt7KcMxD9ldsJyjZM1Wp/model-context-protocol-mcp-and-amazon-bedrock)

[Model Context Protocol servers](https://github.com/modelcontextprotocol/servers)

[Langchain.js MCP Adapter](https://www.linkedin.com/posts/langchain_mcp-adapters-released-introducing-our-activity-7308925375160467457-_BPL/?utm_source=share&utm_medium=member_android&rcm=ACoAAA5jTp0BX-JuOkof3Ak56U3VlXjQVT43NzQ)

[Using LangChain With Model Context Protocol (MCP)](https://cobusgreyling.medium.com/using-langchain-with-model-context-protocol-mcp-e89b87ee3c4c)

  
[Desktop Commander MCP](https://github.com/wonderwhy-er/DesktopCommanderMCP)

[Smithery](https://smithery.ai/)
