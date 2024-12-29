import pandas as pd

class load_drugs:
    
    file_path:str = 'drugs/drug_files/all_drugs.csv'
    
    def __init__(self):
        self.data:pd.DataFrame = self.load_csv_file() # type: ignore
        
    def load_csv_file(self):
        try:
            return pd.read_csv(self.file_path)
        except FileNotFoundError:
            print(f"Error: File not found at {self.file_path}")
            return None

    def get_medicine_link(self, field_name: str) -> str:
        if field_name.lower() in self.data["Medicine name"].str.lower().values:
            return self.data.loc[self.data["Medicine name"].str.lower() == field_name.lower(), "Medicine Link"].values[0]
        else:
            return "Medicine does not exist in drugs.com." 