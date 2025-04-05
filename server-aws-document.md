# AWS Document MCP Server

[AWS Documentation MCP Server](https://awslabs.github.io/mcp/servers/aws-documentation-mcp-server/)를 참조합니다. 여기서 얻은 config는 아래와 같습니다.

```java
{
  "mcpServers": {
    "awslabs.aws-documentation-mcp-server": {
        "command": "uvx",
        "args": ["awslabs.aws-documentation-mcp-server@latest"],
        "env": {
          "FASTMCP_LOG_LEVEL": "ERROR"
        },
        "disabled": false,
        "autoApprove": []
    }
  }
}
```

이때 얻어진 tool에 대한 정보는 아래와 같습니다.

```java
[
   StructuredTool("name=""read_documentation",
   "description=""Fetch and convert an AWS documentation page to markdown format.\n\n## Usage\n\nThis tool retrieves the content of an AWS documentation page and converts it to markdown format.\nFor long documents, you can make multiple calls with different start_index values to retrieve\nthe entire content in chunks.\n\n## URL Requirements\n\n- Must be from the docs.aws.amazon.com domain\n- Must end with .html\n\n## Example URLs\n\n- https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html\n- https://docs.aws.amazon.com/lambda/latest/dg/lambda-invocation.html\n\n## Output Format\n\nThe output is formatted as markdown text with:\n- Preserved headings and structure\n- Code blocks for examples\n- Lists and tables converted to markdown format\n\n## Handling Long Documents\n\nIf the response indicates the document was truncated, you have several options:\n\n1. **Continue Reading**: Make another call with start_index set to the end of the previous response\n2. **Stop Early**: For very long documents (>30,000 characters), if you've already found the specific information needed, you can stop reading\n\nArgs:\n    ctx: MCP context for logging and error handling\n    url: URL of the AWS documentation page to read\n    max_length: Maximum number of characters to return\n    start_index: On return output starting at this character index\n\nReturns:\n    Markdown content of the AWS documentation\n",
   "args_schema="{
      "properties":{
         "url":{
            "anyOf":[
               {
                  "format":"uri",
                  "minLength":1,
                  "type":"string"
               },
               {
                  "type":"string"
               }
            ],
            "description":"URL of the AWS documentation page to read",
            "title":"Url"
         },
         "max_length":{
            "default":5000,
            "description":"Maximum number of characters to return.",
            "exclusiveMaximum":1000000,
            "exclusiveMinimum":0,
            "title":"Max Length",
            "type":"integer"
         },
         "start_index":{
            "default":0,
            "description":"On return output starting at this character index, useful if a previous fetch was truncated and more content is required.",
            "minimum":0,
            "title":"Start Index",
            "type":"integer"
         }
      },
      "required":[
         "url"
      ],
      "title":"read_documentationArguments",
      "type":"object"
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x1279fa8e0>),
   "StructuredTool(name=""search_documentation",
   "description=""Search AWS documentation using the official AWS Documentation Search API.\n\n## Usage\n\nThis tool searches across all AWS documentation for pages matching your search phrase.\nUse it to find relevant documentation when you don\\'t have a specific URL.\n\n## Search Tips\n\n- Use specific technical terms rather than general phrases\n- Include service names to narrow results (e.g., \"S3 bucket versioning\" instead of just \"versioning\")\n- Use quotes for exact phrase matching (e.g., \"AWS Lambda function URLs\")\n- Include abbreviations and alternative terms to improve results\n\n## Result Interpretation\n\nEach result includes:\n- rank_order: The relevance ranking (lower is more relevant)\n- url: The documentation page URL\n- title: The page title\n- context: A brief excerpt or summary (if available)\n\n## Follow-up Actions\n\nAfter searching, you can:\n1. Use `read_documentation` to fetch the full content of relevant pages\n2. Make additional searches with refined terms based on what you read, but avoid repeating similar searches\n3. Use `recommend` to find related content for a specific result\n4. If multiple searches don\\'t yield useful results:\n   - Use `recommend` on a related service\\'s landing page\n   - Ask the user for clarifying information about their specific use case\n\nArgs:\n    ctx: MCP context for logging and error handling\n    search_phrase: Search phrase to use\n    limit: Maximum number of results to return\n\nReturns:\n    List of search results with URLs, titles, and context snippets\n",
   "args_schema="{
      "properties":{
         "search_phrase":{
            "description":"Search phrase to use",
            "title":"Search Phrase",
            "type":"string"
         },
         "limit":{
            "default":10,
            "description":"Maximum number of results to return",
            "maximum":50,
            "minimum":1,
            "title":"Limit",
            "type":"integer"
         }
      },
      "required":[
         "search_phrase"
      ],
      "title":"search_documentationArguments",
      "type":"object"
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x1279fb060>),
   "StructuredTool(name=""recommend",
   "description=""Get content recommendations for an AWS documentation page.\n\n## Usage\n\nThis tool provides recommendations for related AWS documentation pages based on a given URL.\nUse it to discover additional relevant content that might not appear in search results.\n\n## Recommendation Types\n\nThe recommendations include four categories:\n\n1. **Highly Rated**: Popular pages within the same AWS service\n2. **New**: Recently added pages within the same AWS service - useful for finding newly released features\n3. **Similar**: Pages covering similar topics to the current page\n4. **Journey**: Pages commonly viewed next by other users\n\n## When to Use\n\n- After reading a documentation page to find related content\n- When exploring a new AWS service to discover important pages\n- To find alternative explanations of complex concepts\n- To discover the most popular pages for a service\n- To find newly released information by using a service's welcome page URL and checking the **New** recommendations\n\n## Finding New Features\n\nTo find newly released information about a service:\n1. Find any page belong to that service, typically you can try the welcome page\n2. Call this tool with that URL\n3. Look specifically at the **New** recommendation type in the results\n\n## Result Interpretation\n\nEach recommendation includes:\n- url: The documentation page URL\n- title: The page title\n- context: A brief description (if available)\n\nArgs:\n    ctx: MCP context for logging and error handling\n    url: URL of the AWS documentation page to get recommendations for\n\nReturns:\n    List of recommended pages with URLs, titles, and context\n",
   "args_schema="{
      "properties":{
         "url":{
            "anyOf":[
               {
                  "format":"uri",
                  "minLength":1,
                  "type":"string"
               },
               {
                  "type":"string"
               }
            ],
            "description":"URL of the AWS documentation page to get recommendations for",
            "title":"Url"
         }
      },
      "required":[
         "url"
      ],
      "title":"recommendArguments",
      "type":"object"
   },
   "response_format=""content_and_artifact",
   coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x1279faa20>)
]
```

그런데 아래처럼 문서 검색에 실패하고 있습니다.


![image](https://github.com/user-attachments/assets/8e33043f-8ec0-4e81-a789-69221ca5783a)
