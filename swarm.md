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
