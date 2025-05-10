# MCP Context7

## 설치 방법

[Context7 MCP - Up-to-date Code Docs For Any Prompt](https://github.com/upstash/context7)을 따라 아래와 같이 MCP를 설치할 수 있습니다.

```python
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

## 주요 기능 

### resolve-library-id 기능

패키지나 라이브러리 이름을 검색해서 Context7과 호환되는 라이브러리 ID를 찾을 수 있습니다. 검색 결과에서 가장 적합한 라이브러리를 선택하는데, 이때 다음과 같은 기준을 고려합니다
- 검색어와의 이름 유사도
- 설명 관련성
- 코드 스니펫 수(문서화 범위)
- GitHub 스타 수(인기도)

### get-library-docs 기능

라이브러리의 최신 문서를 가져올 수 있어요 이 기능을 사용하기 위해서는 먼저 resolve-library-id로 정확한 라이브러리 ID를 얻어야 합니다.
이를 통해, 특정 주제에 대한 문서를 집중적으로 검색할 수 있고, 문서의 양을 토큰 수로 조절할 수 있습니다.
