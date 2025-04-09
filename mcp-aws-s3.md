# MCP를 이용해 Amazon S3를 활용하기

[Sample S3 Model Context Protocol Server](https://github.com/aws-samples/sample-mcp-server-s3/tree/main)을 참조하여 아래와 같이 S3를 활용합니다. 상세한 내용은 [mcp_s3.py](./application/mcp_s3.py)을 참조합니다.

아래는 bucket 리스트를 조회하는 함수입니다.

```python
async def list_buckets(
    start_after: Optional[str] = None,
    max_buckets: Optional[int] = 5,
    region: Optional[str] = "us-west-2"
) -> List[dict]:
    """
    List S3 buckets using async client with pagination
    """
    async with session.client('s3', region_name=region) as s3:
        if configured_buckets:
            # If buckets are configured, only return those
            response = await s3.list_buckets()
            all_buckets = response.get('Buckets', [])
            configured_bucket_list = [
                bucket for bucket in all_buckets
                if bucket['Name'] in configured_buckets
            ]

            if start_after:
                configured_bucket_list = [
                    b for b in configured_bucket_list
                    if b['Name'] > start_after
                ]

            return configured_bucket_list[:max_buckets]
        else:
            # Default behavior if no buckets configured
            response = await s3.list_buckets()
            buckets = response.get('Buckets', [])

            if start_after:
                buckets = [b for b in buckets if b['Name'] > start_after]

            return buckets[:max_buckets]
```

Bucket의 Object 정보를 아래와 같이 조회할 수 있습니다.

```python
async def list_objects(
    bucket_name: str, 
    prefix: Optional[str] = "", 
    max_keys: Optional[int] = 1000,
    region: Optional[str] = "us-west-2"
) -> List[dict]:
    """
    List objects in a specific bucket using async client with pagination
    Args:
        bucket_name: Name of the S3 bucket
        prefix: Object prefix for filtering
        max_keys: Maximum number of keys to return,
        region: Name of the aws region
    """
    if configured_buckets and bucket_name not in configured_buckets:
        logger.warning(f"Bucket {bucket_name} not in configured bucket list")
        return []

    async with session.client('s3', region_name=region) as s3:
        response = await s3.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix,
            MaxKeys=max_keys
        )
        return response.get('Contents', [])
```

리소스에 대한 정보를 조회합니다.

```python
async def list_resources(
    start_after: Optional[str] = None,
    max_buckets: Optional[int] = 10,
    region: Optional[str] = "us-west-2"
) -> List[Resource]:
    """
    List S3 buckets and their contents as resources with pagination
    Args:
        start_after: Start listing after this bucket name
    """
    resources = []
    logger.debug("Starting to list resources")
    
    logger.debug(f"Configured buckets: {configured_buckets}")

    try:
        # Get limited number of buckets
        buckets = await list_buckets(start_after, max_buckets, region)
        logger.debug(f"Processing {len(buckets)} buckets (max: {max_buckets})")

        # limit concurrent operations
        async def process_bucket(bucket):
            bucket_name = bucket['Name']
            logger.debug(f"Processing bucket: {bucket_name}")

            try:
                # List objects in the bucket with a reasonable limit
                objects = await list_objects(bucket_name, max_keys=1000)

                for obj in objects:
                    if 'Key' in obj and not obj['Key'].endswith('/'):
                        object_key = obj['Key']
                        mime_type = "text/plain" if is_text_file(object_key) else "text/markdown"

                        resource = Resource(
                            uri=f"s3://{bucket_name}/{object_key}",
                            name=object_key,
                            mimeType=mime_type
                        )
                        resources.append(resource)
                        logger.debug(f"Added resource: {resource.uri}")

            except Exception as e:
                logger.error(f"Error listing objects in bucket {bucket_name}: {str(e)}")

        # Use semaphore to limit concurrent bucket processing
        semaphore = asyncio.Semaphore(3)  # Limit concurrent bucket processing
        async def process_bucket_with_semaphore(bucket):
            async with semaphore:
                await process_bucket(bucket)

        # Process buckets concurrently
        await asyncio.gather(*[process_bucket_with_semaphore(bucket) for bucket in buckets])

    except Exception as e:
        logger.error(f"Error listing buckets: {str(e)}")
        raise

    logger.info(f"Returning {len(resources)} resources")
    return resources
```    

## 실행 결과

"내 s3의 bucket 리스트를 알려주세요."와 같이 입력후 결과를 확인합니다. 

![image](https://github.com/user-attachments/assets/2e6f5a6f-5ca7-4d9e-b401-a64171b65c56)

아래와 같이 특정 S3 bucket의 정보를 조회할 수 있습니다.

![image](https://github.com/user-attachments/assets/70b02242-c98c-486a-840a-ccc4f54ee721)
