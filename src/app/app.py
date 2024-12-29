from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from fastapi import FastAPI
import config.config as config
import tools.llm_tools as llm_tools 
from controller.api_controller import api_input_message_format, chat_history_format, api_response_format

tools = llm_tools

llm = ChatOpenAI(model="gpt-4o-mini", api_key=config.get_oai_key())
llm_with_tools = llm.bind_tools(tools.tools)

system_message = """ 
You are a chatbot which answer questions only about medicines.
Here are the rules:
- On each of your answers you must provide a source for the information you provide.
- You must only use the information provided by the tools.
- You can use the tools provided to you to help you answer the questions.
- When the user asks a question you use FDA API to get the information about the medicine and only use that information.
- After mentioning your source, you can also offer a link to the drugs.com page of the medicine if the link is provided.
- If the question is not about a medicine, you must forward to the user and ask if they have any questions about medicines.

Example:
Question: What is the purpose of Entyvio?
Answer: The purpose of Entyvio is to treat ulcerative colitis. (This information is retrieved from the FDA API's). 
        If you want to know more about Entyvio, you can visit the following link: https://www.drugs.com/entyvio.html
"""

app = FastAPI()

def parse_chat_history(chat_history: chat_history_format, user_message) -> list:
    messages = []
    for message in chat_history.messages:
        if message["type"] == "system":
            messages.append(SystemMessage(message["content"]))
        elif message["type"] == "assistant":
            messages.append(AIMessage(message["content"]))
        else:
            messages.append(HumanMessage(message["content"]))
    messages.append(HumanMessage(user_message))
    return messages

@app.post("/chat")
def chat(message: api_input_message_format, chat_history: chat_history_format):
    messages = [SystemMessage(system_message), HumanMessage(message.message)]

    if chat_history.messages != []:
        messages = parse_chat_history(chat_history, message.message)
    else:
        chat_history.messages = [{"type": "system", "content": system_message}]

    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)
    functions_called = []
    for tool_call in ai_msg.tool_calls: # type: ignore
        selected_tool = tools.selected_tool[tool_call["name"].lower()]
        functions_called.append(selected_tool.name)
        tool_msg = selected_tool.invoke(tool_call)
        messages.append(tool_msg)
    resp = llm_with_tools.invoke(messages)

    chat_history.messages.append({"type": "user", "content": message.message})
    chat_history.messages.append({"type": "assistant", "content": str(resp.content)})
    return api_response_format(response=str(resp.content), chat_history=chat_history, functions_called=functions_called)