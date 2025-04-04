## Obsidian MCP Server

여기서는 [Obsidian Model Context Protocol](https://github.com/smithery-ai/mcp-obsidian)을 이용합니다. 

### Obsidian 설치

[Download and install Obsidian](https://help.obsidian.md/install)에서 OS에 맞는 Obsidian을 설치합니다.

### MCP config

[Smithery - mcp-obsidian](https://smithery.ai/server/mcp-obsidian)에 접속하여 자신의 Obsidian 노트의 경로를 입력하고 config를 생성합니다.

![image](https://github.com/user-attachments/assets/88f6bcac-4bd1-4781-af24-736c11acc689)

이렇게 얻어진 config는 아래와 같습니다.

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

### MCP 서버 접속후 검색

접속된 서버의 tool에 대한 정보는 아래와 같습니다.

```java
[
   StructuredTool("name=""read_notes",
   "description=""Read the contents of multiple notes. Each note's content is returned with its path as a reference. Failed reads for individual notes won't stop the entire operation. Reading too many at once may result in an error.",
   "args_schema="{
      "type":"object",
      "properties":{
         "paths":{
            "type":"array",
            "items":{
               "type":"string"
            }
         }
      },
      "required":[
         "paths"
      ],
      "additionalProperties":false,
      "$schema":"http://json-schema.org/draft-07/schema#"
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x119f51bc0>),
   "StructuredTool(name=""search_notes",
   "description=""Searches for a note by its name. The search is case-insensitive and matches partial names. Queries can also be a valid regex. Returns paths of the notes that match the query.",
   "args_schema="{
      "type":"object",
      "properties":{
         "query":{
            "type":"string"
         }
      },
      "required":[
         "query"
      ],
      "additionalProperties":false,
      "$schema":"http://json-schema.org/draft-07/schema#"
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x119f507c0>)
]"chat.py":"164 | models":[
   {
      "bedrock_region":"us-west-2",
      "model_type":"claude",
      "model_id":"anthropic.claude-3-5-sonnet-20241022-v2:0"
   },
   {
      "bedrock_region":"us-east-1",
      "model_type":"claude",
      "model_id":"us.anthropic.claude-3-5-sonnet-20241022-v2:0"
   },
   {
      "bedrock_region":"us-east-2",
      "model_type":"claude",
      "model_id":"us.anthropic.claude-3-5-sonnet-20241022-v2:0"
   }
]
```


아래와 같이 "CSAT 풀었던 결과는?"라고 질의하면, 내 컴퓨터의 Obsidian 메모의 내용을 참조하여 답변합니다.

![image](https://github.com/user-attachments/assets/5c83eee1-262d-428e-97d7-fac3d9f38f2a)

