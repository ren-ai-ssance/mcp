# MCP를 이용한 AWS 로그 분석

[CloudWatch Logs MCP Server](https://github.com/serkanh/cloudwatch-logs-mcp/blob/main/main.py)을 참조하여 아래와 같이 로그 분석을 수행하였습니다. 상세한 코드는 [mcp_log.py](./application/mcp_log.py)을 참조합니다.

CloudWatch의 로그 그룹을 조회합니다.

```python
async def list_groups(
    prefix: Optional[str] = None,
    region: Optional[str] = 'us-west-2'
) -> str:
    """List available CloudWatch log groups."""

    log_client = boto3.client(
        service_name='logs',
        region_name=region
    )

    kwargs = {}
    if prefix:
        kwargs["logGroupNamePrefix"] = prefix

    response = log_client.describe_log_groups(**kwargs)
    log_groups = response.get("logGroups", [])

    # Format the response
    formatted_groups = []
    for group in log_groups:
        formatted_groups.append(
            {
                "logGroupName": group.get("logGroupName"),
                "creationTime": group.get("creationTime"),
                "storedBytes": group.get("storedBytes"),
            }
        )

    response_json = json.dumps(formatted_groups, ensure_ascii=True)

    return response_json
```

아래와 같이 로그를 불러 올 수 있습니다.

```python
async def get_logs(
    logGroupName: str,
    logStreamName: Optional[str] = None,
    startTime: Optional[str] = None,
    endTime: Optional[str] = None,
    filterPattern: Optional[str] = None,
    region: Optional[str] = 'us-west-2'
) -> str:
    """Get CloudWatch logs from a specific log group and stream."""
    logger.info(
        f"Getting CloudWatch logs for group: {logGroupName}, stream: {logStreamName}, "
        f"startTime: {startTime}, endTime: {endTime}, filterPattern: {filterPattern}, "
        f"region: {region}"
    )

    log_client = boto3.client(
        service_name='logs',
        region_name=region
    )

    # Parse start and end times
    start_time_ms = None
    if startTime:
        start_time_ms = _parse_relative_time(startTime)

    end_time_ms = None
    if endTime:
        end_time_ms = _parse_relative_time(endTime)

    # Get logs
    kwargs = {
        "logGroupName": logGroupName,
    }

    if logStreamName:
        kwargs["logStreamNames"] = [logStreamName]

    if filterPattern:
        kwargs["filterPattern"] = filterPattern

    if start_time_ms:
        kwargs["startTime"] = start_time_ms

    if end_time_ms:
        kwargs["endTime"] = end_time_ms

    # Use filter_log_events for more flexible querying
    response = log_client.filter_log_events(**kwargs)
    events = response.get("events", [])

    # Format the response
    formatted_events = []
    for event in events:
        timestamp = event.get("timestamp")
        if timestamp:
            try:
                timestamp = datetime.fromtimestamp(timestamp / 1000).isoformat()
            except Exception:
                timestamp = str(timestamp)

        formatted_events.append(
            {
                "timestamp": timestamp,
                "message": event.get("message"),
                "logStreamName": event.get("logStreamName"),
            }
        )    

    response_json = json.dumps(formatted_events, ensure_ascii=True, default=str)
    return response_json
```

### 실행 결과

"현재 cloudwatch 로그 리스트는?"로 질문합니다. 

![image](https://github.com/user-attachments/assets/80a8f4c4-1f3f-4195-a160-fbc631cf028b)


"/aws/lambda/lambda-rag-for-mcp-rag에서 에러가 있다면 내용을 열거해주세요."라고 질문후에 답변을 확인합니다. 

![image](https://github.com/user-attachments/assets/bfa9056b-5096-4fde-9418-93de95e4d695)

"ClientError에 대해 좀더 설명해주세요."로 입력후 결과를 확인합니다.

![image](https://github.com/user-attachments/assets/77d9f488-c797-4671-9cc4-0f56345b4173)

![image](https://github.com/user-attachments/assets/24d36d23-6c7a-421f-9f9c-342846ae30bf)



![noname](https://github.com/user-attachments/assets/3fcebff9-1442-4d4e-8321-cbe058fd231f)
