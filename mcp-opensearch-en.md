# MCP OpenSearch

You can use OpenSearch with MCP as described in [Unlocking agentic AI experiences with OpenSearch](https://opensearch.org/blog/unlocking-agentic-ai-experiences-with-opensearch/).

## Connection Method

### Supported OpenSearch

The supported OpenSearch versions are as follows. As of June 2025, OpenSearch Serverless appears to be unsupported.

```text
OpenSearch cluster, either self-managed or Amazon OpenSearch Service
```

### Configuration Information for Connection

Configure MCP as follows. The Domain endpoint can be found in the [OpenSearch Console](https://us-west-2.console.aws.amazon.com/aos/home?region=us-west-2#opensearch).

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

## Parsing Results

The SearchIndexTool results start with "Search results from", so you need to split by ':' and use the content after it.

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

In this case, the format of hits in the JSON is as follows. Here we only use text and metadata.

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
      "text":"Image Analysis Report: Korean Text Interpretation and Error Code Resolution Guide for Boiler Deep Switch Error\n\n[Image Summary]\nImage Analysis\n\nThe image contains text in Korean. The text explains content related to a boiler deep switch error.\n\n## Text Content Interpretation\n\nThe text in the image conveys the following information:\n\n\"This is the error code that appears when there is an abnormality in the boiler deep switch. If it continues to appear even after checking the deep switch, you need to contact the service center for repair.\"\n\n## Analysis Based on Reference Information\n\nAccording to the provided reference information, this content explains the solution for boiler error code A, which occurs when there is a problem with the deep switch. The image provides guidance to users to check the deep switch and contact the service center if the error persists.",
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

Therefore, we extract and use it as docs as follows:

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

## Execution Results

Currently supported tools include ListIndexTool, IndexMappingTool, SearchIndexTool, and GetShardsTool.

![mcp-opensearch2_en](https://github.com/user-attachments/assets/535c0288-6df5-4c99-a2df-2387022b33bb)
