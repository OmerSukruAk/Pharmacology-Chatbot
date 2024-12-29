from langchain_core.tools import tool
import requests
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import available_json_fields
import drugs_com_info

availablefields = available_json_fields.fields_loader()
drugscom = drugs_com_info.load_drugs()

def get_valid_fields_in_json(search_arr:list, dict_example:dict) -> list:
    """Returns the valid fields for a given search array and dictionary example."""
    
    return [dict_example[key] for key in search_arr if key in dict_example.keys()]


def get_drug_info(drug_name) -> dict : 

  try:
    url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{drug_name}"

    response = requests.get(url)
    response.raise_for_status()

    return response.json()

  except requests.exceptions.RequestException as e:
    print(f"Error fetching drug information: {e}")
    return {"Error":"Error fetching drug information: {e}"}

def tool_template(medicine_name, field_name, text):
    search_arr = availablefields.get_field_variations(field_name)
    drugs_com_med_link = drugscom.get_medicine_link(medicine_name)
    json_response = get_drug_info(medicine_name)

    if "results" in json_response and json_response["results"]:
        abuse_arr = get_valid_fields_in_json(search_arr, json_response["results"][0])
        if abuse_arr != []: return f"The {text} information of {medicine_name} are {str(abuse_arr)}. This information is retrieved from the FDA API's. If you want to know more about {medicine_name}, you can visit the following link: {drugs_com_med_link}"
    return f"There is no information available for {medicine_name}'s {text} information. Do not answer to the users message. This information is retrieved from the FDA API's. If you want to know more about {medicine_name}, you can visit the following link: {drugs_com_med_link}"

@tool
def when_to_use_medicine(medicine_name: str) -> str:
    """Returns the purpose of the medicine."""
    return tool_template(medicine_name, "when_to_use", "purpose")

@tool 
def when_not_to_use_medicine(medicine_name: str) -> str:
    """Returns the purpose of the medicine."""
    return tool_template(medicine_name, "when_not_to_use", "when not to use")

@tool
def get_medicine_side_effects(medicine_name:str) -> str:
    """Returns the side effects of the medicine."""
    return tool_template(medicine_name, "side_effects", "side effects")

@tool 
def can_be_used_while_pregnancy(medicine_name: str) -> str:
    """Returns whether the medicine can be used during pregnancy."""
    return tool_template(medicine_name, "pregnancy", "pregnancy information")

@tool
def get_medicine_ingredients (medicine_name:str) -> str:
    """Returns the ingredients of the medicine."""
    return tool_template(medicine_name, "ingredients", "ingredients")
    
@tool
def how_to_use_medicine(medicine_name:str) -> str:
    """Returns the usage instructions of the medicine."""
    return tool_template(medicine_name, "how_to_use", "usage instructions")
    
@tool
def what_is_the_abuse_and_overdosage_in_medicine(medicine_name:str) -> str:
    """Returns the abuse and overdosage information of the medicine."""
    return tool_template(medicine_name, "abuse_and_overdosage", "abuse and overdosage information")

load_dotenv()
oai_key = os.getenv("OPENAI_API_KEY")

tools = [
    when_to_use_medicine,
    when_not_to_use_medicine,
    get_medicine_side_effects,
    can_be_used_while_pregnancy,
    get_medicine_ingredients,
    how_to_use_medicine,
    what_is_the_abuse_and_overdosage_in_medicine
    ]



llm = ChatOpenAI(model="gpt-4o-mini", api_key=oai_key) # type: ignore

llm_with_tools = llm.bind_tools(tools)

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

query = "How can I use Ibuprofen?"

messages = [SystemMessage(system_message), HumanMessage(query)]

ai_msg = llm_with_tools.invoke(messages)

print(ai_msg.tool_calls) # type: ignore

messages.append(ai_msg)
print(ai_msg)
message = []
for tool_call in ai_msg.tool_calls: # type: ignore
    selected_tool = {
        "when_to_use_medicine":when_to_use_medicine,
        "when_not_to_use_medicine": when_not_to_use_medicine,
        "get_medicine_side_effects":get_medicine_side_effects,
        "can_be_used_while_pregnancy":can_be_used_while_pregnancy,
        "get_medicine_ingredients":get_medicine_ingredients,
        "how_to_use_medicine":how_to_use_medicine,
        "what_is_the_abuse_and_overdosage_in_medicine":what_is_the_abuse_and_overdosage_in_medicine
        }[tool_call["name"].lower()]
    tool_msg = selected_tool.invoke(tool_call)
    
    messages.append(tool_msg)
    print(messages[-1],end="\n=============\n")

print("______________________")
resp = llm_with_tools.invoke(messages)
print(resp.content)