## Playwright MCP Server

[playwright-mcp](https://github.com/microsoft/playwright-mcp)을 이용하여 웹 페이지와 상호작용할 수 있도록 돕는 구조화된 접근성 스냅샷을 활용합니다. [Playwright MCP Config](https://github.com/microsoft/playwright-mcp?tab=readme-ov-file#example-config)에 접속하여 config를 가져옵니다.

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

이를 이용해 얻어진 tool의 정보는 아래와 같습니다. 

```java
[
   StructuredTool("name=""browser_navigate",
   "description=""Navigate to a URL",
   "args_schema="{
      "type":"object",
      "properties":{
         "url":{
            "type":"string",
            "description":"The URL to navigate to"
         }
      },
      "required":[
         "url"
      ],
      "additionalProperties":false,
      "$schema":"http://json-schema.org/draft-07/schema#"
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x12b0ce7a0>),
   "StructuredTool(name=""browser_go_back",
   "description=""Go back to the previous page",
   "args_schema="{
      "type":"object",
      "properties":{
         
      },
      "additionalProperties":false,
      "$schema":"http://json-schema.org/draft-07/schema#"
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x12b0ce980>),
   "StructuredTool(name=""browser_go_forward",
   "description=""Go forward to the next page",
   "args_schema="{
      "type":"object",
      "properties":{
         
      },
      "additionalProperties":false,
      "$schema":"http://json-schema.org/draft-07/schema#"
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x12b0cea20>),
   "StructuredTool(name=""browser_choose_file",
   "description=""Choose one or multiple files to upload",
   "args_schema="{
      "type":"object",
      "properties":{
         "paths":{
            "type":"array",
            "items":{
               "type":"string"
            },
            "description":"The absolute paths to the files to upload. Can be a single file or multiple files."
         }
      },
      "required":[
         "paths"
      ],
      "additionalProperties":false,
      "$schema":"http://json-schema.org/draft-07/schema#"
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x12b0ceac0>),
   "StructuredTool(name=""browser_snapshot",
   "description=""Capture accessibility snapshot of the current page, this is better than screenshot",
   "args_schema="{
      "type":"object",
      "properties":{
         
      },
      "additionalProperties":false,
      "$schema":"http://json-schema.org/draft-07/schema#"
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x12b0ceb60>),
   "StructuredTool(name=""browser_click",
   "description=""Perform click on a web page",
   "args_schema="{
      "type":"object",
      "properties":{
         "element":{
            "type":"string",
            "description":"Human-readable element description used to obtain permission to interact with the element"
         },
         "ref":{
            "type":"string",
            "description":"Exact target element reference from the page snapshot"
         }
      },
      "required":[
         "element",
         "ref"
      ],
      "additionalProperties":false,
      "$schema":"http://json-schema.org/draft-07/schema#"
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x12b0cec00>),
   "StructuredTool(name=""browser_hover",
   "description=""Hover over element on page",
   "args_schema="{
      "type":"object",
      "properties":{
         "element":{
            "type":"string",
            "description":"Human-readable element description used to obtain permission to interact with the element"
         },
         "ref":{
            "type":"string",
            "description":"Exact target element reference from the page snapshot"
         }
      },
      "required":[
         "element",
         "ref"
      ],
      "additionalProperties":false,
      "$schema":"http://json-schema.org/draft-07/schema#"
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x12b0ceca0>),
   "StructuredTool(name=""browser_type",
   "description=""Type text into editable element",
   "args_schema="{
      "type":"object",
      "properties":{
         "element":{
            "type":"string",
            "description":"Human-readable element description used to obtain permission to interact with the element"
         },
         "ref":{
            "type":"string",
            "description":"Exact target element reference from the page snapshot"
         },
         "text":{
            "type":"string",
            "description":"Text to type into the element"
         },
         "submit":{
            "type":"boolean",
            "description":"Whether to submit entered text (press Enter after)"
         }
      },
      "required":[
         "element",
         "ref",
         "text",
         "submit"
      ],
      "additionalProperties":false,
      "$schema":"http://json-schema.org/draft-07/schema#"
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x12b0ced40>),
   "StructuredTool(name=""browser_select_option",
   "description=""Select an option in a dropdown",
   "args_schema="{
      "type":"object",
      "properties":{
         "element":{
            "type":"string",
            "description":"Human-readable element description used to obtain permission to interact with the element"
         },
         "ref":{
            "type":"string",
            "description":"Exact target element reference from the page snapshot"
         },
         "values":{
            "type":"array",
            "items":{
               "type":"string"
            },
            "description":"Array of values to select in the dropdown. This can be a single value or multiple values."
         }
      },
      "required":[
         "element",
         "ref",
         "values"
      ],
      "additionalProperties":false,
      "$schema":"http://json-schema.org/draft-07/schema#"
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x12b0cede0>),
   "StructuredTool(name=""browser_take_screenshot",
   "description=""Take a screenshot of the current page. You can't perform actions based on the screenshot, use browser_snapshot for actions.",
   "args_schema="{
      "type":"object",
      "properties":{
         "raw":{
            "type":"boolean",
            "description":"Whether to return without compression (in PNG format). Default is false, which returns a JPEG image."
         }
      },
      "additionalProperties":false,
      "$schema":"http://json-schema.org/draft-07/schema#"
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x12b0cee80>),
   "StructuredTool(name=""browser_press_key",
   "description=""Press a key on the keyboard",
   "args_schema="{
      "type":"object",
      "properties":{
         "key":{
            "type":"string",
            "description":"Name of the key to press or a character to generate, such as `ArrowLeft` or `a`"
         }
      },
      "required":[
         "key"
      ],
      "additionalProperties":false,
      "$schema":"http://json-schema.org/draft-07/schema#"
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x12b0cef20>),
   "StructuredTool(name=""browser_wait",
   "description=""Wait for a specified time in seconds",
   "args_schema="{
      "type":"object",
      "properties":{
         "time":{
            "type":"number",
            "description":"The time to wait in seconds"
         }
      },
      "required":[
         "time"
      ],
      "additionalProperties":false,
      "$schema":"http://json-schema.org/draft-07/schema#"
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x12b0cefc0>),
   "StructuredTool(name=""browser_save_as_pdf",
   "description=""Save page as PDF",
   "args_schema="{
      "type":"object",
      "properties":{
         
      },
      "additionalProperties":false,
      "$schema":"http://json-schema.org/draft-07/schema#"
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x12b0cf060>),
   "StructuredTool(name=""browser_close",
   "description=""Close the page",
   "args_schema="{
      "type":"object",
      "properties":{
         
      },
      "additionalProperties":false,
      "$schema":"http://json-schema.org/draft-07/schema#"
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x12b0cf100>),
   "StructuredTool(name=""browser_install",
   "description=""Install the browser specified in the config. Call this if you get an error about the browser not being installed.",
   "args_schema="{
      "type":"object",
      "properties":{
         
      },
      "additionalProperties":false,
      "$schema":"http://json-schema.org/draft-07/schema#"
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x12b0cf1a0>)
]
```

이제 "https://github.com/kyopark2014/technical-summary/blob/main/api-gateway-log.md를 참조하여 로깅에 대한 정보를 정리하세요."와 같이 입력하면, 해당 URL을 열어서 관련정보를 가져온 후에 아래와 같이 답변합니다.

![image](https://github.com/user-attachments/assets/fe7c4382-9c8c-4cd7-9c0e-166fa04bc71e)
