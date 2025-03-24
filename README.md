# Model Context Protocol

MCP(Model Context Protocal)은 Anthropic에서 기여하고 있는 오픈소스 프로젝트입니다. 출시이후에 엄청난 속도로 사용자와 서버군을 넓혀가고 있습니다.

[MCP with LangChain](https://tirendazacademy.medium.com/mcp-with-langchain-cabd6199e0ac)을 참조합니다.

```text
pip install langchain-mcp-adapters
```

### Build Your Own Server

```python
# Build an MCP server
from mcp.server.fastmcp import FastMCP 

# Initialize the class
mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
  return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
  return a * b

if __name__ == "__main__":
  # Start a process that communicates via standard input/output
  mcp.run(transwhaport="stdio")
```

### Build Your Own Client

```python
from mcp import ClientSession, StdioServerParameters

server_params = StdioServerParameters(
  command="python",
  args=["math_server.py"],
)

from mcp.client.stdio import stdio_client

async def run_agent():
  async with stdio_client(server_params) as (read, write):
    # Open an MCP session to interact with the math_server.py tool.
    async with ClientSession(read, write) as session:
      # Initialize the session.
      await session.initialize()
      # Load tools
      tools = await load_mcp_tools(session)
      # Create a ReAct agent.
      agent = create_react_agent(model, tools)
      # Run the agent.
      agent_response = await agent.ainvoke(
        # Now, let's give our message.
       {"messages": "what's (4 + 6) x 14?"})
      # Return the response.
      return agent_response["messages"][3].content

if __name__ == "__main__":
  result = asyncio.run(run_agent())
  print(result)
```

### MCP Servers

[Model Context Protocol servers](https://github.com/modelcontextprotocol/servers)에서 쓸만한 서버군을 찾아봅니다. 

- [Perplexity Ask MCP Server](https://github.com/ppl-ai/modelcontextprotocol)
- [Riza MCP Server](https://github.com/riza-io/riza-mcp)
- [Tavily MCP Server](https://github.com/tavily-ai/tavily-mcp)


## Reference 

[Using MCP with LangGraph agents](https://www.youtube.com/watch?v=OX89LkTvNKQ)

[MCP From Scratch](https://mirror-feeling-d80.notion.site/MCP-From-Scratch-1b9808527b178040b5baf83a991ed3b2)

[Understanding MCP From Scratch](https://www.youtube.com/watch?v=CDjjaTALI68)

[LangChain MCP Adapters](https://github.com/langchain-ai/langchain-mcp-adapters)


[MCP - For Server Developers](https://modelcontextprotocol.io/quickstart/server)

[Model Context Protocol (MCP) and Amazon Bedrock](https://community.aws/content/2uFvyCPQt7KcMxD9ldsJyjZM1Wp/model-context-protocol-mcp-and-amazon-bedrock)

[Model Context Protocol servers](https://github.com/modelcontextprotocol/servers)

[Langchain.js MCP Adapter](https://www.linkedin.com/posts/langchain_mcp-adapters-released-introducing-our-activity-7308925375160467457-_BPL/?utm_source=share&utm_medium=member_android&rcm=ACoAAA5jTp0BX-JuOkof3Ak56U3VlXjQVT43NzQ)


[MCP with LangChain](https://tirendazacademy.medium.com/mcp-with-langchain-cabd6199e0ac)

[Using LangChain With Model Context Protocol (MCP)(https://cobusgreyling.medium.com/using-langchain-with-model-context-protocol-mcp-e89b87ee3c4c)

  
