import json

class fields_loader:
    
    file_path:str = 'drugs/fields/fields_without_table.json'
    
    def __init__(self):
        self.data:dict = self.read_fields_json() # type: ignore
        
    def read_fields_json(self):
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            print(f"Error: File not found at {self.file_path}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON data in {self.file_path}: {e}")
            return None
    
    def get_field_variations(self, field_name:str) -> list:
        if field_name in self.data["fields"].keys():
            return self.data["fields"][field_name]
        else:
            return "Field does not exist. If you want to use that field, please add it to the fields.json file."  # type: ignore
