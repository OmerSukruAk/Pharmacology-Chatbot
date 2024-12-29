from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from fastapi import FastAPI
from pydantic import BaseModel
import config.config as config
import tools.llm_tools as llm_tools 

tools = llm_tools

llm = ChatOpenAI(model="gpt-4o-mini", api_key=config.get_oai_key())

llm_with_tools = llm.bind_tools(tools.tools)

system_message = """"
You are a chatbot which answer questions about medicines.
Here are the rules:
- On each of your answers you must provide a source for the information you provide.
- You must only use the information provided by the tools.
- You can use the tools provided to you to help you answer the questions.
- After mentioning your source, you can also offer a link to the drugs.com page of the medicine if the link is provided.

Example:
Question: What is the purpose of Entyvio?
Answer: The purpose of Entyvio is to treat ulcerative colitis. (This information is retrieved from the FDA API's). 
        If you want to know more about Entyvio, you can visit the following link: https://www.drugs.com/entyvio.html
"""

app = FastAPI()

class Message(BaseModel):
    message: str

class ChatHistory(BaseModel):
    messages: list[dict]

class Response(BaseModel):
    response: str
    chat_history: ChatHistory


def parse_chat_history(chat_history: ChatHistory, user_message) -> list:
    messages = []
    for message in chat_history.messages:
        print(message)
        if message["type"] == "system":
            messages.append(SystemMessage(message["content"]))
        elif message["type"] == "assistant":
            messages.append(AIMessage(message["content"]))
        else:
            messages.append(HumanMessage(message["content"]))
    messages.append(HumanMessage(user_message))
    return messages

@app.post("/chat")
def chat(message: Message, chat_history: ChatHistory):
    messages = [SystemMessage(system_message), HumanMessage(message.message)]

    if chat_history.messages != [{}]:
        messages = parse_chat_history(chat_history,message.message)
    else:
        chat_history.messages = [{"type": "system", "content": system_message}]

    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)
    for tool_call in ai_msg.tool_calls: # type: ignore
        selected_tool = tools.selected_tool[tool_call["name"].lower()]
        tool_msg = selected_tool.invoke(tool_call)
        messages.append(tool_msg)
    resp = llm_with_tools.invoke(messages)

    chat_history.messages.append({"type": "user", "content": message.message})
    chat_history.messages.append({"type": "assistant", "content": str(resp.content)})
    return Response(response=str(resp.content), chat_history=chat_history)

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, port=8000)