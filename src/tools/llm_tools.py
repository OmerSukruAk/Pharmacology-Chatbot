from langchain_core.tools import tool
from controller.drug_controller import tool_template

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



tools = [
        when_to_use_medicine,
        when_not_to_use_medicine,
        get_medicine_side_effects,
        can_be_used_while_pregnancy,
        get_medicine_ingredients,
        how_to_use_medicine,
        what_is_the_abuse_and_overdosage_in_medicine
    ]

selected_tool = {
        "when_to_use_medicine":when_to_use_medicine,
        "when_not_to_use_medicine": when_not_to_use_medicine,
        "get_medicine_side_effects":get_medicine_side_effects,
        "can_be_used_while_pregnancy":can_be_used_while_pregnancy,
        "get_medicine_ingredients":get_medicine_ingredients,
        "how_to_use_medicine":how_to_use_medicine,
        "what_is_the_abuse_and_overdosage_in_medicine":what_is_the_abuse_and_overdosage_in_medicine
        }