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

## 결과의 parsing

SearchIndexTool의 결과는 아래와 같이 "Search reasult from"으로 시작하므로 ':'을 이하를 잘라서 사용하여야 합니다.

```java
Search results from [index name]:
{
  "took": 4,
  "timed_out": false,
  "_shards": {
    "total": 5,
    "successful": 5,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 5,
      "relation": "eq"
    },
    "max_score": null,
    "hits": [....]
  }
}
```

이때 json에서 hits의 포맷은 아래와 같습니다. 여기서 text와 metadata만 활용합니다. 

```java
{
   "_index":"agentic-rag",
   "_id":"510ef5f0-3821-4a31-8a14-795e6942e4d8",
   "_score":16.0109,
   "_source":{
      "vector_field":[
         0.010811034590005875,
         -0.007020711898803711,
         (skip....)
         0.0017551779747009277
      ],
      "text":"이미지 분석 보고서: 보일러 딥스위치 오류 관련 한국어 텍스트 해석 및 에러코드 해결 안내\n\n[이미지 요약]\n용 분석\n\n이미지에는 한국어로 된 텍스트가 포함되어 있습니다. 텍스트는 보일러 딥스위치 오류에 관한 내용을 설명하고 있습니다.\n\n## 텍스트 내용 해석\n\n이미지에 있는 텍스트는 다음과 같은 내용을 전달하고 있습니다:\n\n\"보일러 딥스위치 이상이 생기면 나오는 에러코드 입니다. 딥스위치를 확인해준 후에도 계속 뜬다면 서비스 센터에 연락하셔서 고쳐야 합니다.\"\n\n## 참고 정보 기반 분석\n\n제공된 참고 정보에 따르면, 이 내용은 보일러 에러 코드 A에 관한 해결책을 설명하는 것으로, 딥스위치에 문제가 있을 때 발생하는 오류입니다. 이미지는 사용자에게 딥스위치를 확인하고, 오류가 지속될 경우 서비스 센터에 연락하라는 안내를 제공하고 있습니다.",
      "metadata":{
         "name":"docs/captures/error_code.pdf/img_error_code_3.png",
         "page":"3",
         "url":"https://d16smec4ijjs8n.cloudfront.net/docs/captures/error_code.pdf/img_error_code_3.png",
         "parent_doc_id":"87ed4eab-079f-4fed-9e7f-3e2bbc94349d",
         "doc_level":"child"
      }
   }
}
```

따라서, 아래와 같이 docs로 추출하여 활용합니다.

```python
docs = []
if tool_name == "SearchIndexTool":
    if ":" in tool_content:
        extracted_json_data = tool_content.split(":", 1)[1].strip()
        logger.info(f"extracted_json_data: {extracted_json_data}")
        try:
            json_data = json.loads(extracted_json_data)
            logger.info(f"extracted_json_data: {extracted_json_data[:200]}")
        except json.JSONDecodeError:
            logger.info("JSON parsing error")
            json_data = {}
    else:
        json_data = {}

    if "hits" in json_data:
        hits = json_data["hits"]["hits"]
        logger.info(f"hits[0]: {hits[0]}")

        for hit in hits:
            text = hit["_source"]["text"]
            metadata = hit["_source"]["metadata"]

            docs.append({
                "text": text,
                "metadata": metadata
            })
    logger.info(f"docs: {docs}")
```

## 실행 결과

현재 지원되는 tool에는 ListIndexTool, IndexMappingTool, SearchIndexTool, GetShardsTool이 있습니다.

![mcp-opensearch2](https://github.com/user-attachments/assets/e359e12d-6a33-41a0-8f7b-c82aa1bb85d5)
