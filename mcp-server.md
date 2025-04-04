# MCP Servers

## ArXiv MCP Server

[ArXiv MCP Server](https://github.com/blazickjp/arxiv-mcp-server)는 [Smithery-arxiv-mcp-server]에 접속해서 아래와 같은 configuration 가져옵니다.

![image](https://github.com/user-attachments/assets/200fc7e4-5edc-45dc-b476-aa2f99aa50e3)

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

Local에서 실행시 uv를 설치합니다.

```text
brew install uv
```

arxiv-mcp-server을 설치합니다. 

```text
uv tool install arxiv-mcp-server
```

app에 접속하여 config를 업데이트하고 아래와 같이 "ReAct Agent란?"라고 입력후 답변을 확인하였습니다. 

이때 가져온 Tool에 대한 정보는 아래와 같습니다.

```java
"chat.py":"1395 | tools":[
   "StructuredTool(name=""search_papers",
   "description=""Search for papers on arXiv with advanced filtering",
   "args_schema="{
      "type":"object",
      "properties":{
         "query":{
            "type":"string"
         },
         "max_results":{
            "type":"integer"
         },
         "date_from":{
            "type":"string"
         },
         "date_to":{
            "type":"string"
         },
         "categories":{
            "type":"array",
            "items":{
               "type":"string"
            }
         }
      },
      "required":[
         "query"
      ]
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x134314e00>),
   "StructuredTool(name=""download_paper",
   "description=""Download a paper and create a resource for it",
   "args_schema="{
      "type":"object",
      "properties":{
         "paper_id":{
            "type":"string",
            "description":"The arXiv ID of the paper to download"
         },
         "check_status":{
            "type":"boolean",
            "description":"If true, only check conversion status without downloading",
            "default":false
         }
      },
      "required":[
         "paper_id"
      ]
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x134314cc0>),
   "StructuredTool(name=""list_papers",
   "description=""List all existing papers available as resources",
   "args_schema="{
      "type":"object",
      "properties":{
         
      },
      "required":[
         
      ]
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x134314c20>),
   "StructuredTool(name=""read_paper",
   "description=""Read the full content of a stored paper in markdown format",
   "args_schema="{
      "type":"object",
      "properties":{
         "paper_id":{
            "type":"string",
            "description":"The arXiv ID of the paper to read"
         }
      },
      "required":[
         "paper_id"
      ]
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x134314b80>)
]
```

실행결과는 아래와 같습니다. 얻어온 tool에는 'search_papers', 'download_paper', 'list_papers', 'read_paper'가 있습니다.

![image](https://github.com/user-attachments/assets/ac8cae0e-fd7a-4565-aa99-4605297ddeb2)





