from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
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

query = "Is Ibuprofen okay to use if a woman is pregnant?"

messages = [SystemMessage(system_message), HumanMessage(query)]

ai_msg = llm_with_tools.invoke(messages)

print(ai_msg.tool_calls) # type: ignore

messages.append(ai_msg)
print(ai_msg)
message = []
for tool_call in ai_msg.tool_calls: # type: ignore
    selected_tool = tools.selected_tool[tool_call["name"].lower()]
    tool_msg = selected_tool.invoke(tool_call)
    
    messages.append(tool_msg)
    print(messages[-1],end="\n=============\n")

print("______________________")
resp = llm_with_tools.invoke(messages)
print(resp.content)