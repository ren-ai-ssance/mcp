# MCP Knowledge Bases

Knowledge Bases를 이용하면 손쉽게 RAG구성하고 편리하게 사용할 수 있습니다.

[Amazon Bedrock Knowledge Base Retrieval MCP Server](https://github.com/awslabs/mcp/tree/main/src/bedrock-kb-retrieval-mcp-server)에서는 KB_INCLUSION_TAG_KEY에 tag를 지정하면 Knowledge base를 찾아서 RAG로 활용할 수 있습니다. 

그런데, 여기서 knowledgebases_resource이 MCP resources로 지정되어 있어서, query_knowledge_bases_tool가 knowledge_base_id를 가져오지 못하는 문제점이 있습니다. 따라서, [mcp_server_kb.py](./application/mcp_server_kb.py)에서는 아래와 같이 설정을 바꾸고 MCP 서버를 설정합니다.


```python
@mcp.tool(name='GetKnowledgeBases')
async def knowledgebases_resource() -> str:
    """List all available Amazon Bedrock Knowledge Bases and their data sources.

    This resource returns a mapping of knowledge base IDs to their details, including:
    - name: The human-readable name of the knowledge base
    - data_sources: A list of data sources within the knowledge base, each with:
      - id: The unique identifier of the data source
      - name: The human-readable name of the data source

    ## Example response structure:
    ```json
    {
        "kb-12345": {
            "name": "Customer Support KB",
            "data_sources": [
                {"id": "ds-abc123", "name": "Technical Documentation"},
                {"id": "ds-def456", "name": "FAQs"}
            ]
        },
        "kb-67890": {
            "name": "Product Information KB",
            "data_sources": [
                {"id": "ds-ghi789", "name": "Product Specifications"}
            ]
        }
    }
    ```

    ## How to use this information:
    1. Extract the knowledge base IDs (like "kb-12345") for use with the QueryKnowledgeBases tool
    2. Note the data source IDs if you want to filter queries to specific data sources
    3. Use the names to determine which knowledge base and data source(s) are most relevant to the user's query
    """
    kb_list = json.dumps(await discover_knowledge_bases(kb_agent_mgmt_client, kb_inclusion_tag_key))
    logger.info(f"kb_list: {kb_list}")
    return kb_list
```

이를 MCP로 등록하는것은 아래 config를 따릅니다.

```java
{
    "mcpServers": {
        "aws_knowledge_base": {
            "command": "python",
            "args": [
                "application/mcp_server_kb.py"
            ],
            "env": {
                "KB_INCLUSION_TAG_KEY": "mcp-rag"
            }
        }
    }
}
```

Knowledge Base는 KB_INCLUSION_TAG_KEY에 해당하는 "mcp-rag" tag를 아래와 같이 "true"로 설정하여야 합니다.

![image](https://github.com/user-attachments/assets/f1ccc54b-35d2-4910-8902-ff3cd7cf5d99)


이때의 결과는 아래와 같습니다. GetKnowledgeBases로 tag가 설정된 Knowledge Base를 검색한 후에 QueryKnowledgeBases로 관련된 문서를 가져옵니다. 

![image](https://github.com/user-attachments/assets/66eeadea-23a6-4721-ba91-922db27b745c)


