import models.drugs_available_json_fields as drugs_available_json_fields
import models.drugs_com_info as drugs_com_info
from models.fda_drug_api_client import get_drug_info

availablefields = drugs_available_json_fields.fields_loader()
drugscom = drugs_com_info.load_drugs()

def get_valid_fields_in_json(search_arr:list, dict_example:dict) -> list:
    """Returns the valid fields for a given search array and dictionary example."""
    
    return [dict_example[key] for key in search_arr if key in dict_example.keys()]

def tool_template(medicine_name, field_name, text):
    search_arr = availablefields.get_field_variations(field_name)
    drugs_com_med_link = drugscom.get_medicine_link(medicine_name)
    json_response = get_drug_info(medicine_name)

    if "results" in json_response and json_response["results"]:
        abuse_arr = get_valid_fields_in_json(search_arr, json_response["results"][0])
        if abuse_arr != []: return f"The {text} information of {medicine_name} are {str(abuse_arr)}. This information is retrieved from the FDA API's. If you want to know more about {medicine_name}, you can visit the following link: {drugs_com_med_link}"
    return f"There is no information available for {medicine_name}'s {text} information. Do not answer to the users message. This information is retrieved from the FDA API's. If you want to know more about {medicine_name}, you can visit the following link: {drugs_com_med_link}"
