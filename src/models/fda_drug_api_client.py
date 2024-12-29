import requests

def get_drug_info(drug_name) -> dict : 

  try:
    url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{drug_name}"

    response = requests.get(url)
    response.raise_for_status()

    return response.json()

  except requests.exceptions.RequestException as e:
    print(f"Error fetching drug information: {e}")
    return {"Error":"Error fetching drug information: {e}"}