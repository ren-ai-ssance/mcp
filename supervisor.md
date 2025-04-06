# LangGraph Supervisor

[LangGraph Multi-Agent Supervisor](https://github.com/langchain-ai/langgraph-supervisor-py)을 이용하면 hierachical 구조를 만들때 도움이 됩니다.


이를 위해 langgraph-supervisor을 설치합니다.

```text
pip install langgraph-supervisor
```




## 실행 결과

"서울 날씨는?"로 입력후 결과를 확인합니다.

<img width="700" alt="image" src="https://github.com/user-attachments/assets/1a55e7cd-fa4a-466d-b0ec-e71b47ff2c76" />


"strawberry의 r의 갯수는?

<img width="700" alt="image" src="https://github.com/user-attachments/assets/3936683e-1057-466b-93b4-8ee968f1ceac" />





"서울에서 부산을 거쳐서 제주로 가려고합니다. 가는 동안의 날씨와 지역 맛집 검색해서 추천해주세요."로 입력후 결과를 확인합니다. 

<img width="700" alt="image" src="https://github.com/user-attachments/assets/f6d55fbc-186e-461d-9366-f1326417e2ed" />


동작은 아래와 같습니다.

![image](https://github.com/user-attachments/assets/b7ec2913-804b-4b4a-a1a9-d972ddb9a591)




app = workflow.compile(
    checkpointer=checkpointer,
    store=store
)
```
