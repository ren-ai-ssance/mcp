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

  
