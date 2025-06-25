import logging
import sys
import json
import traceback
import chat
import utils

from langgraph.prebuilt import ToolNode
from typing import Literal
from langgraph.graph import START, END, StateGraph
from typing_extensions import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

logging.basicConfig(
    level=logging.INFO,  
    format='%(filename)s:%(lineno)d | %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger("agent")

config = utils.load_config()
sharing_url = config["sharing_url"] if "sharing_url" in config else None
s3_prefix = "docs"
capture_prefix = "captures"

status_msg = []
def get_status_msg(status):
    global status_msg
    status_msg.append(status)

    if status != "end)":
        status = " -> ".join(status_msg)
        return "[status]\n" + status + "..."
    else: 
        status = " -> ".join(status_msg)
        return "[status]\n" + status

response_msg = []
references = []
image_urls = []

def get_tool_info(tool_name, tool_content):
    tool_references = []    
    urls = []
    content = ""

    # tavily
    if isinstance(tool_content, str) and "Title:" in tool_content and "URL:" in tool_content and "Content:" in tool_content:
        logger.info("Tavily parsing...")
        items = tool_content.split("\n\n")
        for i, item in enumerate(items):
            # logger.info(f"item[{i}]: {item}")
            if "Title:" in item and "URL:" in item and "Content:" in item:
                try:
                    title_part = item.split("Title:")[1].split("URL:")[0].strip()
                    url_part = item.split("URL:")[1].split("Content:")[0].strip()
                    content_part = item.split("Content:")[1].strip().replace("\n", "")
                    
                    logger.info(f"title_part: {title_part}")
                    logger.info(f"url_part: {url_part}")
                    logger.info(f"content_part: {content_part}")

                    content += f"{content_part}\n\n"
                    
                    tool_references.append({
                        "url": url_part,
                        "title": title_part,
                        "content": content_part[:100] + "..." if len(content_part) > 100 else content_part
                    })
                except Exception as e:
                    logger.info(f"Parsing error: {str(e)}")
                    continue                

    # OpenSearch
    elif tool_name == "SearchIndexTool": 
        if ":" in tool_content:
            extracted_json_data = tool_content.split(":", 1)[1].strip()
            try:
                json_data = json.loads(extracted_json_data)
                # logger.info(f"extracted_json_data: {extracted_json_data[:200]}")
            except json.JSONDecodeError:
                logger.info("JSON parsing error")
                json_data = {}
        else:
            json_data = {}
        
        if "hits" in json_data:
            hits = json_data["hits"]["hits"]
            if hits:
                logger.info(f"hits[0]: {hits[0]}")

            for hit in hits:
                text = hit["_source"]["text"]
                metadata = hit["_source"]["metadata"]
                
                content += f"{text}\n\n"

                filename = metadata["name"].split("/")[-1]
                # logger.info(f"filename: {filename}")
                
                content_part = text.replace("\n", "")
                tool_references.append({
                    "url": metadata["url"], 
                    "title": filename,
                    "content": content_part[:100] + "..." if len(content_part) > 100 else content_part
                })
                
        logger.info(f"content: {content}")
        
    # Knowledge Base
    elif tool_name == "QueryKnowledgeBases": 
        try:
            # Handle case where tool_content contains multiple JSON objects
            if tool_content.strip().startswith('{'):
                # Parse each JSON object individually
                json_objects = []
                current_pos = 0
                brace_count = 0
                start_pos = -1
                
                for i, char in enumerate(tool_content):
                    if char == '{':
                        if brace_count == 0:
                            start_pos = i
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0 and start_pos != -1:
                            try:
                                json_obj = json.loads(tool_content[start_pos:i+1])
                                # logger.info(f"json_obj: {json_obj}")
                                json_objects.append(json_obj)
                            except json.JSONDecodeError:
                                logger.info(f"JSON parsing error: {tool_content[start_pos:i+1][:100]}")
                            start_pos = -1
                
                json_data = json_objects
            else:
                # Try original method
                json_data = json.loads(tool_content)                
            # logger.info(f"json_data: {json_data}")

            # Build content
            if isinstance(json_data, list):
                for item in json_data:
                    if isinstance(item, dict) and "content" in item:
                        content_text = item["content"].get("text", "")
                        content += content_text + "\n\n"

                        uri = "" 
                        if "location" in item:
                            if "s3Location" in item["location"]:
                                uri = item["location"]["s3Location"]["uri"]
                                # logger.info(f"uri (list): {uri}")
                                ext = uri.split(".")[-1]

                                # ext가 이미지라면 
                                url = sharing_url + "/" + s3_prefix + "/" + uri.split("/")[-1]
                                if ext in ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "ico", "webp"]:
                                    url = sharing_url + "/" + capture_prefix + "/" + uri.split("/")[-1]
                                logger.info(f"url: {url}")
                                
                                tool_references.append({
                                    "url": url, 
                                    "title": uri.split("/")[-1],
                                    "content": content_text[:100] + "..." if len(content_text) > 100 else content_text
                                })          
                
        except json.JSONDecodeError as e:
            logger.info(f"JSON parsing error: {e}")
            json_data = {}
            content = tool_content  # Use original content if parsing fails

        logger.info(f"content: {content}")
        logger.info(f"tool_references: {tool_references}")

    # aws document
    elif tool_name == "search_documentation":
        try:
            json_data = json.loads(tool_content)
            for item in json_data:
                logger.info(f"item: {item}")
                
                if isinstance(item, str):
                    try:
                        item = json.loads(item)
                    except json.JSONDecodeError:
                        logger.info(f"Failed to parse item as JSON: {item}")
                        continue
                
                if isinstance(item, dict) and 'url' in item and 'title' in item:
                    url = item['url']
                    title = item['title']
                    content_text = item['context'][:100] + "..." if len(item['context']) > 100 else item['context']
                    tool_references.append({
                        "url": url,
                        "title": title,
                        "content": content_text
                    })
                else:
                    logger.info(f"Invalid item format: {item}")
                    
        except json.JSONDecodeError:
            logger.info(f"JSON parsing error: {tool_content}")
            pass

        logger.info(f"content: {content}")
        logger.info(f"tool_references: {tool_references}")
            
    # ArXiv
    elif tool_name == "search_papers" and "papers" in tool_content:
        try:
            json_data = json.loads(tool_content)

            papers = json_data['papers']
            for paper in papers:
                url = paper['url']
                title = paper['title']
                abstract = paper['abstract'].replace("\n", "")
                content_text = abstract[:100] + "..." if len(abstract) > 100 else abstract
                content += f"{content_text}\n\n"
                logger.info(f"url: {url}, title: {title}, content: {content_text}")

                tool_references.append({
                    "url": url,
                    "title": title,
                    "content": content_text
                })
        except json.JSONDecodeError:
            logger.info(f"JSON parsing error: {tool_content}")
            pass

        logger.info(f"content: {content}")
        logger.info(f"tool_references: {tool_references}")

    else:        
        try:
            if isinstance(tool_content, dict):
                json_data = tool_content
            else:
                json_data = json.loads(tool_content)
            
            logger.info(f"json_data: {json_data}")
            if isinstance(json_data, dict) and "path" in json_data:  # path
                path = json_data["path"]
                if isinstance(path, list):
                    for url in path:
                        urls.append(url)
                else:
                    urls.append(path)            

            for item in json_data:
                logger.info(f"item: {item}")
                if "reference" in item and "contents" in item:
                    url = item["reference"]["url"]
                    title = item["reference"]["title"]
                    content_text = item["contents"][:100] + "..." if len(item["contents"]) > 100 else item["contents"]
                    tool_references.append({
                        "url": url,
                        "title": title,
                        "content": content_text
                    })
            logger.info(f"tool_references: {tool_references}")

        except json.JSONDecodeError:
            pass

    return content, urls, tool_references

class State(TypedDict):
    messages: Annotated[list, add_messages]
    image_url: list

async def call_model(state: State, config):
    logger.info(f"###### call_model ######")

    last_message = state['messages'][-1]
    logger.info(f"last message: {last_message}")
    
    image_url = state['image_url'] if 'image_url' in state else []

    status_container = config.get("configurable", {}).get("status_container", None)
    response_container = config.get("configurable", {}).get("response_container", None)
    tools = config.get("configurable", {}).get("tools", None)
    system_prompt = config.get("configurable", {}).get("system_prompt", None)
    
    if isinstance(last_message, ToolMessage):
        tool_name = last_message.name
        tool_content = last_message.content
        logger.info(f"tool_name: {tool_name}, content: {tool_content[:800]}")

        if chat.debug_mode == "Enable":
            response_container.info(f"{tool_name}: {str(tool_content)}")
            response_msg.append(f"{tool_name}: {str(tool_content)}")

        global references
        content, urls, refs = get_tool_info(tool_name, tool_content)
        if refs:
            for r in refs:
                references.append(r)
            logger.info(f"refs: {refs}")
        if urls:
            for url in urls:
                image_url.append(url)
            logger.info(f"urls: {urls}")

            if chat.debug_mode == "Enable":
                response_container.info(f"Added path to image_url: {urls}")
                response_msg.append(f"Added path to image_url: {urls}")

        if content:  # manupulate the output of tool message
            messages = state["messages"]
            messages[-1] = ToolMessage(
                name=tool_name,
                tool_call_id=last_message.tool_call_id,
                content=content
            )
            state["messages"] = messages

        if chat.debug_mode == "Enable":
            response_container.info(f"{tool_name}: {tool_content[:800]}")
            response_msg.append(f"{tool_name}: {tool_content[:800]}")

    if isinstance(last_message, AIMessage) and last_message.content:
        if chat.debug_mode == "Enable":
            status_container.info(get_status_msg(f"{last_message.name}"))
            response_container.info(f"{last_message.content[:800]}")
            response_msg.append(last_message.content[:800])    
    
    if system_prompt:
        system = system_prompt
    else:
        system = (
            "당신의 이름은 서연이고, 질문에 친근한 방식으로 대답하도록 설계된 대화형 AI입니다."
            "상황에 맞는 구체적인 세부 정보를 충분히 제공합니다."
            "모르는 질문을 받으면 솔직히 모른다고 말합니다."
            "한국어로 답변하세요."
        )

    chatModel = chat.get_chat(extended_thinking=chat.reasoning_mode)
    model = chatModel.bind_tools(tools)

    try:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        chain = prompt | model
            
        response = await chain.ainvoke(state["messages"])
        logger.info(f"response of call_model: {response}")

    except Exception:
        response = AIMessage(content="답변을 찾지 못하였습니다.")

        err_msg = traceback.format_exc()
        logger.info(f"error message: {err_msg}")

    return {"messages": [response], "image_url": image_url}

async def should_continue(state: State, config) -> Literal["continue", "end"]:
    logger.info(f"###### should_continue ######")

    messages = state["messages"]    
    last_message = messages[-1]

    status_container = config.get("configurable", {}).get("status_container", None)
    response_container = config.get("configurable", {}).get("response_container", None)
    key_container = config.get("configurable", {}).get("key_container", None)
    
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        tool_name = last_message.tool_calls[-1]['name']
        logger.info(f"--- CONTINUE: {tool_name} ---")

        tool_args = last_message.tool_calls[-1]['args']

        if last_message.content:
            logger.info(f"last_message: {last_message.content}")
            if chat.debug_mode == "Enable":
                response_container.info(f"{last_message.content}")
                response_msg.append(last_message.content)

        logger.info(f"tool_name: {tool_name}, tool_args: {tool_args}")
        if chat.debug_mode == "Enable":
            key_container.info(f"{tool_name}: {tool_args}")
        
        if chat.debug_mode == "Enable":
            status_container.info(get_status_msg(f"{tool_name}"))
            if "code" in tool_args:
                logger.info(f"code: {tool_args['code']}")
                response_container.code(tool_args['code'])
                response_msg.append(f"{tool_args['code']}")

        return "continue"
    else:
        if chat.debug_mode == "Enable":
            status_container.info(get_status_msg("end)"))

        logger.info(f"--- END ---")
        return "end"

def buildChatAgent(tools):
    tool_node = ToolNode(tools)

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

    return workflow.compile() 

def buildChatAgentWithHistory(tools):
    tool_node = ToolNode(tools)

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

    return workflow.compile(
        checkpointer=chat.checkpointer,
        store=chat.memorystore
    )

def extract_reference(response):
    references = []
    for i, re in enumerate(response):
        if isinstance(re, ToolMessage):
            logger.info(f"###### extract_reference ######")
            try: 
                
                # check json format
                if isinstance(re.content, str) and (re.content.strip().startswith('{') or re.content.strip().startswith('[')):
                    tool_result = json.loads(re.content)
                    # logger.info(f"tool_result: {tool_result}")
                else:
                    tool_result = re.content
                    # logger.info(f"tool_result (not JSON): {tool_result[:200]}")

                
                                
                if isinstance(tool_result, list):
                    logger.info(f"size of tool_result: {len(tool_result)}")
                    for i, item in enumerate(tool_result):
                        logger.info(f'item[{i}]: {item}')
                        
                        # RAG
                        if "reference" in item:
                            logger.info(f"reference: {item['reference']}")

                            infos = item['reference']
                            url = infos['url']
                            title = infos['title']
                            source = infos['from']
                            logger.info(f"url: {url}, title: {title}, source: {source}")

                            references.append({
                                "url": url,
                                "title": title,
                                "content": item['contents'][:100].replace("\n", "")
                            })

                        # Others               
                        if isinstance(item, str):
                            try:
                                item = json.loads(item)

                                # AWS Document
                                if "rank_order" in item:
                                    references.append({
                                        "url": item['url'],
                                        "title": item['title'],
                                        "content": item['context'][:100].replace("\n", "")
                                  })
                            except json.JSONDecodeError:
                                logger.info(f"JSON parsing error: {item}")
                                continue

            except:
                logger.info(f"fail to parsing..")
                pass
    return references

async def run(question, tools, status_container, response_container, key_container, historyMode):
    global status_msg, response_msg, references, image_urls
    status_msg = []
    response_msg = []
    references = []
    image_urls = []

    if chat.debug_mode == "Enable":
        status_container.info(get_status_msg("(start"))

    if historyMode == "Enable":
        app = buildChatAgentWithHistory(tools)
        config = {
            "recursion_limit": 50,
            "configurable": {"thread_id": chat.userId},
            "status_container": status_container,
            "response_container": response_container,
            "key_container": key_container,
            "tools": tools
        }
    else:
        app = buildChatAgent(tools)
        config = {
            "recursion_limit": 50,
            "status_container": status_container,
            "response_container": response_container,
            "key_container": key_container,
            "tools": tools
        }
    
    inputs = {
        "messages": [HumanMessage(content=question)]
    }

    value = result = None
    async for output in app.astream(inputs, config):
        for key, value in output.items():
            logger.info(f"--> key: {key}, value: {value}")

            if key == "messages":
                if isinstance(value, dict) and "messages" in value:
                    message = value["messages"]
                elif isinstance(value, list):
                    value = {"messages": value, "image_url": []}
                    message = value["messages"]
                else:
                    value = {"messages": [value], "image_url": []}
                    message = value["messages"]

                refs = extract_reference(message)
                if refs:
                    for r in refs:
                        references.append(r)
                        logger.info(f"r: {r}")
                
    if value and "messages" in value and len(value["messages"]) > 0:
        result = value["messages"][-1].content
    else:
        result = "답변을 찾지 못하였습니다."

    logger.info(f"references: {references}")
    if references:
        ref = "\n\n### Reference\n"
        for i, reference in enumerate(references):
            ref += f"{i+1}. [{reference['title']}]({reference['url']}), {reference['content']}...\n"    
        result += ref

    image_url = value["image_url"] if value and "image_url" in value else []

    return result, image_url

async def run_task(question, tools, system_prompt, status_container, response_container, key_container, historyMode, previous_status_msg, previous_response_msg):
    global status_msg, response_msg
    status_msg = previous_status_msg
    response_msg = previous_response_msg
    global references
    references = []
    image_urls = []

    if chat.debug_mode == "Enable":
        status_container.info(get_status_msg("(start"))

    if historyMode == "Enable":
        app = buildChatAgentWithHistory(tools)
        config = {
            "recursion_limit": 50,
            "configurable": {"thread_id": chat.userId},
            "status_container": status_container,
            "response_container": response_container,
            "key_container": key_container,
            "tools": tools,
            "system_prompt": system_prompt
        }
    else:
        app = buildChatAgent(tools)
        config = {
            "recursion_limit": 50,
            "status_container": status_container,
            "response_container": response_container,
            "key_container": key_container,
            "tools": tools,
            "system_prompt": system_prompt
        }

    value = None
    inputs = {
        "messages": [HumanMessage(content=question)]
    }

    final_output = None
    async for output in app.astream(inputs, config):
        for key, value in output.items():
            logger.info(f"--> key: {key}, value: {value}")
            
            if key == "messages":
                if isinstance(value, dict) and "messages" in value:
                    message = value["messages"]
                elif isinstance(value, list):
                    value = {"messages": value, "image_url": []}
                    message = value["messages"]
                else:
                    value = {"messages": [value], "image_url": []}
                    message = value["messages"]

                refs = extract_reference(message)
                if refs:
                    for r in refs:
                        references.append(r)
                        logger.info(f"r: {r}")
                
    if value and "messages" in value and len(value["messages"]) > 0:
        result = value["messages"][-1].content
    else:
        result = "답변을 찾지 못하였습니다."

    image_url = final_output["image_url"] if final_output and "image_url" in final_output else []

    return result, image_url, status_msg, response_msg