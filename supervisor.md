# Supervisor Agent를 이용한 Multi-Agent Collaboration

## Multi Agent Supervisor

[Multi-agent supervisor](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/)에서는 Router형태의 supervisor를 구현합니다.

아래와 같이 structured output에서는 router class를 이용하여 agent를 선택하고 있습니다.

```python
class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""

    next: Literal[*options]

def supervisor_node(state: State) -> Command[Literal[*members, "__end__"]]:
    messages = [
        {"role": "system", "content": system_prompt},
    ] + state["messages"]
    response = llm.with_structured_output(Router).invoke(messages)
    goto = response["next"]
    if goto == "FINISH":
        goto = END

    return Command(goto=goto, update={"next": goto})
```

## LangGraph Supervisor

[LangGraph Multi-Agent Supervisor](https://github.com/langchain-ai/langgraph-supervisor)을 이용하면 hierachical 구조를 만들때 도움이 됩니다.

[LangGraph Multi-Agent Supervisor](https://github.com/langchain-ai/langgraph-supervisor-py)



이를 위해 langgraph-supervisor을 설치합니다.

```text
pip install langgraph-supervisor
```



동작은 아래와 같습니다.

![image](https://github.com/user-attachments/assets/b7ec2913-804b-4b4a-a1a9-d972ddb9a591)

사용 예는 아래와 같습니다.

```python
# Create supervisor workflow
workflow = create_supervisor(
    [research_agent, math_agent],
    model=model,
    prompt=(
        "You are a team supervisor managing a research expert and a math expert. "
        "For current events, use research_agent. "
        "For math problems, use math_agent."
    )
)

# Compile and run
app = workflow.compile()
result = app.invoke({
    "messages": [
        {
            "role": "user",
            "content": "what's the combined headcount of the FAANG companies in 2024?"
        }
    ]
})
```

output에서 response는 아래와 같이 full_history, last_message와 같이 선택가능합니다.

```python
workflow = create_supervisor(
    agents=[agent1, agent2],
    output_mode="full_history"
)
```


## Swarm

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
app = workflow.compile(
    checkpointer=checkpointer,
    store=store
)
```
