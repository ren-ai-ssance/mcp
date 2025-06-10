# MCP OpenSearch

You can use OpenSearch with MCP as described in [Unlocking agentic AI experiences with OpenSearch](https://opensearch.org/blog/unlocking-agentic-ai-experiences-with-opensearch/).

## Connection Method

### Supported OpenSearch

The supported OpenSearch versions are as follows. As of June 2025, OpenSearch Serverless appears to be unsupported.

```text
OpenSearch cluster, either self-managed or Amazon OpenSearch Service
```

### Configuration Information for Connection

Configure MCP as follows. Note that OPENSEARCH_INDEX must be included. The Domain endpoint can be found in the [OpenSearch Console](https://us-west-2.console.aws.amazon.com/aos/home?region=us-west-2#opensearch).

```java
{
    "mcpServers": {
        "opensearch-mcp-server": {
            "command": "uvx",
            "args": [
                "opensearch-mcp-server-py"
            ],
            "env": {
                "OPENSEARCH_URL": "domain endpoint",
                "AWS_REGION":"us-west-2",
                "OPENSEARCH_USERNAME":"username", 
                "OPENSEARCH_PASSWORD":"password",
                "OPENSEARCH_INDEX":"index name"
            }
        }
    }
}    
```

## Execution Results

Currently supported tools include ListIndexTool, IndexMappingTool, SearchIndexTool, and GetShardsTool.

![mcp-opensearch2_en](https://github.com/user-attachments/assets/535c0288-6df5-4c99-a2df-2387022b33bb)
