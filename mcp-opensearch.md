# MCP OpenSearch

[Unlocking agentic AI experiences with OpenSearch](https://opensearch.org/blog/unlocking-agentic-ai-experiences-with-opensearch/)와 같이 MCP로 OpenSearch를 이용할 수 있습니다.

## 접속 방법

### 지원되는 OpenSearch

지원되는 OpenSearch는 아래와 같습니다. 2025.6월 기준으로 OpenSearch Serverless는 미지원으로 보여집니다.

```text
OpenSearch cluster, either self-managed or Amazon OpenSearch Service
```

### 접속하는 Config 정보

MCP 설정은 아래와 같이 수행합니다. Domain endpoint는 [OpenSearch Console](https://us-west-2.console.aws.amazon.com/aos/home?region=us-west-2#opensearch)에서 확인합니다. 

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
                "OPENSEARCH_PASSWORD":"password"
            }
        }
    }
}    
```

## 실행 결과

현재 지원되는 tool에는 ListIndexTool, IndexMappingTool, SearchIndexTool, GetShardsTool이 있습니다.

![mcp-opensearch2](https://github.com/user-attachments/assets/e359e12d-6a33-41a0-8f7b-c82aa1bb85d5)
