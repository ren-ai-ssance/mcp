## Airbnb MCP Server

[Airbnb MCP Server](https://github.com/openbnb-org/mcp-server-airbnb)에 따라 Airbnb를 mcp로 연결할 수 있습니다. [Smithery - Airbnb](https://smithery.ai/server/@openbnb-org/mcp-server-airbnb)에서 config를 가져옵니다. 

config 정보는 아래와 같습니다.

![image](https://github.com/user-attachments/assets/853e1551-e07e-4401-9e8b-052929070c2c)

JSON 정보는 아래와 같습니다. 

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

이때 얻어진 Tool 정보는 아래와 같습니다.

```java
[
   StructuredTool("name=""airbnb_search",
   "description=""Search for Airbnb listings with various filters and pagination. Provide direct links to the user",
   "args_schema="{
      "type":"object",
      "properties":{
         "location":{
            "type":"string",
            "description":"Location to search for (city, state, etc.)"
         },
         "placeId":{
            "type":"string",
            "description":"Google Maps Place ID (overrides the location parameter)"
         },
         "checkin":{
            "type":"string",
            "description":"Check-in date (YYYY-MM-DD)"
         },
         "checkout":{
            "type":"string",
            "description":"Check-out date (YYYY-MM-DD)"
         },
         "adults":{
            "type":"number",
            "description":"Number of adults"
         },
         "children":{
            "type":"number",
            "description":"Number of children"
         },
         "infants":{
            "type":"number",
            "description":"Number of infants"
         },
         "pets":{
            "type":"number",
            "description":"Number of pets"
         },
         "minPrice":{
            "type":"number",
            "description":"Minimum price for the stay"
         },
         "maxPrice":{
            "type":"number",
            "description":"Maximum price for the stay"
         },
         "cursor":{
            "type":"string",
            "description":"Base64-encoded string used for Pagination"
         },
         "ignoreRobotsText":{
            "type":"boolean",
            "description":"Ignore robots.txt rules for this request"
         }
      },
      "required":[
         "location"
      ]
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x125bc3f60>),
   "StructuredTool(name=""airbnb_listing_details",
   "description=""Get detailed information about a specific Airbnb listing. Provide direct links to the user",
   "args_schema="{
      "type":"object",
      "properties":{
         "id":{
            "type":"string",
            "description":"The Airbnb listing ID"
         },
         "checkin":{
            "type":"string",
            "description":"Check-in date (YYYY-MM-DD)"
         },
         "checkout":{
            "type":"string",
            "description":"Check-out date (YYYY-MM-DD)"
         },
         "adults":{
            "type":"number",
            "description":"Number of adults"
         },
         "children":{
            "type":"number",
            "description":"Number of children"
         },
         "infants":{
            "type":"number",
            "description":"Number of infants"
         },
         "pets":{
            "type":"number",
            "description":"Number of pets"
         },
         "ignoreRobotsText":{
            "type":"boolean",
            "description":"Ignore robots.txt rules for this request"
         }
      },
      "required":[
         "id"
      ]
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x125b240e0>)
]
```

이때에 얻어진 결과는 아래와 같습니다.


![image](https://github.com/user-attachments/assets/cde0b053-e699-4b65-8e7c-03eea8f8f9ec)
