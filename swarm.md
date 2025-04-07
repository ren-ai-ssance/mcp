# LangGraph Swarm

[LangGraph Multi-Agent Swarm](https://github.com/langchain-ai/langgraph-swarm-py/tree/main)와 같이 때로는 agent가 직접 메시지 및 history를 공유함으로써 multi-agent를 구성하는것이 좋을수도 있습니다. [Swarm](https://github.com/openai/swarm)은 agent간에 handoff가 가능합니다. 아래에서는 [LangGraph Swarm](https://www.youtube.com/watch?v=iqXn6Oiis4Q)을 참조하여 multi-agent를 구성하는 것을 설명합니다.

아래와 같이 LangGraph의 Swarm을 설치합니다.

```text
pip install langgraph-swarm
```

아래는 추후 구현 예정입니다. 

```python
from langgraph_swarm import create_handoff_tool, create_swarm

checkpointer = InMemorySaver()
store = InMemoryStore()
workflow = create_swarm(
    [search, stock, code_interpreter],
    default_active_agent="search"
)
```
## 실행 결과

"서울 날씨는?"이라고 질문하면 search agent에서 weather agent로 이동 후에 날씨 정보를 조회합니다.

<img src="https://github.com/user-attachments/assets/c7e1e998-aeb1-4bac-b98f-6de05bcc41b2" width="700">


"서울에서 부산을 거쳐서 제주로 가려고합니다. 가는 동안의 현재 온도와 지역 맛집 검색해서 추천해주세요."로 입력후 결과를 확인합니다.

이때의 결과를 보면 아래와 같이, 시작이 search agent이므로 weather agent로 transfer하고 날씨 정보를 수집합니다.

<img src="https://github.com/user-attachments/assets/a5ccda15-862e-42cf-98e4-305e17c6e461" width="700">


날씨 정보를 모두 수집하면 다시 search agent로 전환한 후에 검색을 수행합니다.

<img src="https://github.com/user-attachments/assets/7de5a1a7-5201-4b9a-b7aa-b1e248615338" width="700">


최종적으로 아래와 같이 서울, 부산, 제주의 온도와 맛집에 대한 정보를 아래처럼 수집하였습니다.

<img src="https://github.com/user-attachments/assets/5295485c-6077-4e88-9065-69e3b6b1f185" width="700">

