# LangGraph Supervisor

[LangGraph Multi-Agent Supervisor](https://github.com/langchain-ai/langgraph-supervisor-py)을 이용하면 hierachical 구조를 만들때 도움이 됩니다.

이를 위해 langgraph-supervisor을 설치합니다.

```text
pip install langgraph-supervisor
```

동작은 아래와 같습니다.

![image](https://github.com/user-attachments/assets/b7ec2913-804b-4b4a-a1a9-d972ddb9a591)


아래와 같이 collaborator들을 준비합니다.

```python
search_agent = create_collaborator(
    [tool_use.search_by_tavily, tool_use.search_by_knowledge_base], 
    "search_agent", st
)
stock_agent = create_collaborator(
    [tool_use.stock_data_lookup], 
    "stock_agent", st
)
weather_agent = create_collaborator(
    [tool_use.get_weather_info], 
    "weather_agent", st
)
code_agent = create_collaborator(
    [tool_use.code_drawer, tool_use.code_interpreter], 
    "code_agent", st
)

def create_collaborator(tools, name, st):
    chatModel = chat.get_chat(extended_thinking="Disable")
    model = chatModel.bind_tools(tools)
    tool_node = ToolNode(tools)

    class State(TypedDict): 
        messages: Annotated[list, add_messages]
        name: str

    def should_continue(state: State) -> Literal["continue", "end"]:
        messages = state["messages"]    
        last_message = messages[-1]
        if last_message.tool_calls:
            return "continue"        
        else:
            return "end"
           
    def call_model(state: State, config):
        last_message = state['messages'][-1]
                
        if chat.isKorean(state["messages"][0].content)==True:
            system = (
                "당신의 이름은 서연이고, 질문에 친근한 방식으로 대답하도록 설계된 대화형 AI입니다."
                "상황에 맞는 구체적인 세부 정보를 충분히 제공합니다."
                "모르는 질문을 받으면 솔직히 모른다고 말합니다."
                "한국어로 답변하세요."
            )
        else: 
            system = (            
                "You are a conversational AI designed to answer in a friendly way to a question."
                "If you don't know the answer, just say that you don't know, don't try to make up an answer."
            )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        chain = prompt | model
        response = chain.invoke(state["messages"])
        return {"messages": [response]}

    def buildChatAgent():
        workflow = StateGraph(State)
        workflow.add_node("agent", call_model)
        workflow.add_node("action", tool_node)
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges(
            "agent",
            should_continue,
            {
                "continue": "action",
                "end": END,
            },
        )
        workflow.add_edge("action", "agent")
        return workflow.compile(name=name)
    
    return buildChatAgent()
```

Supervisor agent는 아래와 같이 생성합니다.

```python
from langgraph_supervisor import create_supervisor

workflow = create_supervisor(
    [search_agent, stock_agent, weather_agent, code_agent],
    model=chat.get_chat(extended_thinking="Disable"),
    prompt = (
        "당신의 이름은 서연이고, 질문에 친근한 방식으로 대답하도록 설계된 대화형 AI입니다."
        "상황에 맞는 구체적인 세부 정보를 충분히 제공합니다."
        "모르는 질문을 받으면 솔직히 모른다고 말합니다."
        "한국어로 답변하세요."
    )
)        
supervisor_agent = workflow.compile(name="superviser")
```

아래와 같이 실행합니다.

```python
inputs = [HumanMessage(content=query)]
    config = {
        "recursion_limit": 50
    }
    
    result = supervisor_agent.invoke({"messages": inputs}, config)
    logger.info(f"messages: {result['messages']}")

    msg = result["messages"][-1].content
```

## 실행 결과

"서울 날씨는?"로 입력후 결과를 확인합니다.

<img width="700" alt="image" src="https://github.com/user-attachments/assets/419f8ec9-1533-414a-9fae-f790538623b7" />


"strawberry의 r의 갯수는?

<img width="700" alt="image" src="https://github.com/user-attachments/assets/4f988649-0c2a-499b-abca-1bc9ac6f11dd" />


"서울에서 부산을 거쳐서 제주로 가려고합니다. 가는 동안의 날씨와 지역 맛집 검색해서 추천해주세요."로 입력후 결과를 확인합니다. 

<img width="700" alt="image" src="https://github.com/user-attachments/assets/f6d55fbc-186e-461d-9366-f1326417e2ed" />

