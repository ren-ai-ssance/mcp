# MCP로 RAG Application 구현하기

MCP(Model Context Protocal)은 Anthropic에서 기여하고 있는 오픈소스 프로젝트입니다. 2024년 11월에 MCP가 이렇게 성공할 것으로 예상한 사람은 많지 않았을것 같습니다. 저는 API 기반의 시스템 인터페이스를 선호했기에 MCP는 그다지 매력적이지 않았습니다. 하지만 이제 MCP는 LLM이 외부 context를 가져오는 방법으로 주된 인터페이스가 되었고 향후 이런 방향은 더 가속화될것 입니다. 

[MCP with LangChain](https://github.com/langchain-ai/langchain-mcp-adapters)을 참조합니다.



## MCP 활용

### MCP Basic

사용자는 자신의 Computer에 설치된 Claude Desktop, Cursor와 같은 AI 도구뿐 아니라 주로 Agent형태로 개발된 어플리케이션을 통해 MCP 서버에 연결할 수 있습니다. MCP server는 MCP client의 요청에 자신이 할수 있는 기능을 capability로 제공하고 client의 요청을 수행합니다. MCP server는 local computer의 파일이나 데이터베이스를 조회할 수 있을뿐 아니라 인터넷에 있는 외부 서버의 API를 이용해 필요한 정보를 조회할 수 있습니다. MCP Client는 Server와 JSON-RPC 2.0 프로토콜을 이용해 연결되는데, stdio나 SSE (Server-Sent Events)을 선택하여, Host의 요청을 MCP에 전달할 수 있고, 응답을 받아서 활용할 수 있습니다.  

<img src="https://github.com/user-attachments/assets/f6002b87-1a02-4014-a2bb-358a55dfb73f" width="700">


MCP의 주요 요소의 정의와 동작은 아래와 같습니다.

- MCP Hosts: MCP를 통해 데이터에 접근하려는 프로그램으로 Claude Desktop, Cursor, User Agent Application이 해당됩니다.
- MCP Clients: MCP Server와 1:1로 연결을 수행하는 Client로서 MCP Server와 stdio 또는 SSE 방식으로 연결할 수 있습니다.
- MCP Servers: Client에 자신의 Capability를 알려주는 경량 프로그램으로 Local Computer의 파일이나 데이터베이스를 조회할 수 있고, 외부 API를 이용해 정보를 조회할 수 있습니다.

### LangChain MCP Adapter

[LangChain MCP Adapter](https://github.com/langchain-ai/langchain-mcp-adapters)는 MCP를 LangGraph agent와 함께 사용할 수 있게 해주는 경량의 랩퍼(lightweight wrapper)로서 MIT 기반의 오픈소스입니다. MCP Adapter의 주된 역할은 MCP server를 위한 tool들을 정의하고, MCP client에서 tools의 정보를 조회하고 LangGraph의 tool node로 정의하여 활용할 수 있도록 도와줍니다. 

LangChain MCP Adapter를 아래와 같이 설치합니다.

```text
pip install langchain-mcp-adapters
```

RAG 검색을 위한 MCP server는 아래와 같이 정의할 수 있습니다. 

```python
from mcp.server.fastmcp import FastMCP 

mcp = FastMCP(
    name = "Search",
    instructions=(
        "You are a helpful assistant. "
        "You can search the documentation for the user's question and provide the answer."
    ),
) 

@mcp.tool()
def search(keyword: str) -> str:
    "search keyword"

    return retrieve_knowledge_base(keyword)

if __name__ =="__main__":
    print(f"###### main ######")
    mcp.run(transport="stdio")
```

여기서 RAG 검색은 아래와 같이 lambda를 trigger하는 방식으로 구성하였습니다.

```python
def retrieve_knowledge_base(query):
    lambda_client = boto3.client(
        service_name='lambda',
        region_name=bedrock_region
    )
    functionName = f"lambda-rag-for-{projectName}"
    payload = {
        'function': 'search_rag',
        'knowledge_base_name': knowledge_base_name,
        'keyword': query,
        'top_k': numberOfDocs,
        'grading': "Enable",
        'model_name': model_name,
        'multi_region': multi_region
    }
    output = lambda_client.invoke(
        FunctionName=functionName,
        Payload=json.dumps(payload),
    )
    payload = json.load(output['Payload'])
    return payload['response'], []
```

MCP client는 아래와 같이 실행합니다. 비동기적으로 실행하기 위해서 asyncio를 이용하였습니다. MCP server에 대한 정보는 CDK로 배포후 생성되는 output에서 추출한 config.json 파일에서 얻어옵니다. 이후 사용자가 UI에서 MCP Config를 업데이트하면 정보를 업데이트 할 수 있습니다. 서버 정보는 [langchain-mcp-adapters](https://github.com/langchain-ai/langchain-mcp-adapters)에서 제공하는 MultiServerMCPClient을 이용해 아래와 같이 정의합니다.

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
asyncio.run(mcp_rag_agent_multiple(query, st))

async def mcp_rag_agent_multiple(query, st):
    server_params = load_multiple_mcp_server_parameters()
    async with  MultiServerMCPClient(server_params) as client:
        with st.status("thinking...", expanded=True, state="running") as status:                       
            tools = client.get_tools()
            agent = create_agent(tools)
            response = await agent.ainvoke({"messages": query})
            result = response["messages"][-1].content

        st.markdown(result)
        st.session_state.messages.append({
            "role": "assistant", 
            "content": result
        })
    return result
```

여기서는 custom한 목적으로 사용할 수 있도록 아래와 같이 agent를 정의하였습니다.

```python
def create_agent(tools):
    tool_node = ToolNode(tools)

    chatModel = get_chat(extended_thinking="Disable")
    model = chatModel.bind_tools(tools)

    class State(TypedDict):
        messages: Annotated[list, add_messages]

    def call_model(state: State, config):
        system = (
            "당신의 이름은 서연이고, 질문에 친근한 방식으로 대답하도록 설계된 대화형 AI입니다."
            "상황에 맞는 구체적인 세부 정보를 충분히 제공합니다."
            "모르는 질문을 받으면 솔직히 모른다고 말합니다."
            "한국어로 답변하세요."
        )
        try:
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system),
                    MessagesPlaceholder(variable_name="messages"),
                ]
            )
            chain = prompt | model                
            response = chain.invoke(state["messages"])
        return {"messages": [response]}

    def should_continue(state: State) -> Literal["continue", "end"]:
        messages = state["messages"]    
        last_message = messages[-1]
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            return "continue"        
        else:
            return "end"

    def buildChatAgent():
        workflow = StateGraph(State)
        workflow.add_node("agent", call_model)
        workflow.add_node("action", tool_node)
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges(
            "agent",
            should_continue,
            {
                "continue": "action",
                "end": END,
            },
        )
        workflow.add_edge("action", "agent")
        return workflow.compile() 
    
    return buildChatAgent()
```

## MCP Servers의 활용

[Model Context Protocol servers](https://github.com/modelcontextprotocol/servers)에서 쓸만한 서버군을 찾아봅니다. 

- [Perplexity Ask MCP Server](https://github.com/ppl-ai/modelcontextprotocol)
- [Riza MCP Server](https://github.com/riza-io/riza-mcp)
- [Tavily MCP Server](https://github.com/tavily-ai/tavily-mcp)






## MCP Server 정보 업데이트

[Smithery - Google Search Server](https://smithery.ai/server/@gradusnikov/google-search-mcp-server)는 구글 검색을 제공합니다. 검색엔진 ID와 API Key를 필요로 합니다. 

```java
{
  "mcpServers": {
    "google-search-mcp-server": {
      "command": "npx",
      "args": [
        "-y",
        "@smithery/cli@latest",
        "run",
        "@gradusnikov/google-search-mcp-server",
        "--config",
        "{\"googleCseId\":\"b5cd8c527fbd64b72\",\"googleApiKey\":\"AIzbSyDQlYpck8-9TbBSuxoew1luOGVB6unRPNk\"}"
      ]
    }
  }
}
```

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


### MCP inspector

Development Mode에서 mcp server를 테스트 하기 위해 MCP inspector를 이용할 수 있습니다. 아래와 같이 cli를 설치합니다. 

```text
pip install 'mcp[cli]'
```

이후 아래와 같이 실행하면 쉽게 mcp-server.py의 동작을 테스트 할 수 있습니다. 실행시 http://localhost:5173 와 같은 URL을 제공합니다.

```text
mcp dev mcp-server.py
```


## 실행 결과

### MCP로 RAG를 조회하여 활용하기

[error_code.pdf](./contents/error_code.pdf)을 다운로드 한 후에 파일을 업로드합니다. 이후 아래와 같이 "보일러 에러중 수압과 관련된 에러 코드를 검색해주세요."와 같이 입력하면 mcp를 이용해 tool의 정보를 가져오고, search tool로 얻어진 정보를 이용해 아래와 같은 정보를 보여줄 수 있습니다. 이때 search tool은 lambda를 실행하는데 lambda에서는 완전 관리형 RAG 서비스인 knowledge base를 이용하여 검색어를 조회하고 관련성을 평가한 후에 관련된 문서만을 전달합니다. Agent는 RAG를 조회하여 얻어진 정보로 답변을 아래와 같이 구합니다.

<img src="https://github.com/user-attachments/assets/01b5e47f-ada1-405e-8455-3d3ce260cb41" width="650">

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
        "132c5abd-6f2e-4e42-89a1-d0b1fcb75613"
      ]
    }
  }
}
```

아래는 기본 설정된 RAG를 위한 정보입니다.

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

아래는 multiple mcp server를 설정시 config 입니다.

```python
{
   "mcpServers":{
      "RAG":{
         "command":"python",
         "args":[
            "application/mcp-server.py"
         ]
      },
      "mcp-tavily":{
         "command":"npx",
         "args":[
            "-y",
            "@smithery/cli@latest",
            "run",
            "mcp-tavily",
            "--key",
            "132c5abd-6f2e-4e42-89a1-d0b1fcb75613"
         ]
      }
   }
}
```

이 정보를 아래와 같이 왼쪽 메뉴의 MCP Config에 복사합니다.

<img src="https://github.com/user-attachments/assets/0e054f8e-4356-42e0-a70e-636af8d377c8" width="300">


이후 메뉴에서 "Agent"를 선택후에 아래와 같이 "강남역 맛집은?"라고 입력후 결과를 확인합니다.

<img src="https://github.com/user-attachments/assets/8275bf94-2f46-475d-9eea-02568e70199b" width="650">



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

[Cursor AI 말고, 나만의 #MCP 에이전트 앱 만들어 보기!](https://www.youtube.com/watch?v=ISrYHGg2C2c)
