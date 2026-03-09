import pandas as pd
from PyQt6.QtWidgets import QMessageBox,QTableWidget

def load_table_data(file_path : str, parent_widget : QTableWidget) -> pd.DataFrame:

    if file_path.endswith((".csv",".tsv",".txt")):
        try:
            return pd.read_csv(file_path,sep=None,engine="python")
        
        except Exception as e:
            QMessageBox.critical(
                parent_widget, 
                "System Error", 
                f"Could not read the file")
            print(str(e))
            return None
        
    elif file_path.endswith(".json"):
        try:
            df = pd.read_json(file_path)

            for column in df.columns:
                if any(isinstance(val,(dict,list)) for val in df[column]):
                    raise ValueError("Nested JSON Deteced")
            return df
                
        except ValueError:
            QMessageBox.critical(
            parent_widget, 
            "Invalid Format", 
            "Error: JSON must be a flat array of records. Nested structures are not supported.")
            return None
    
        except Exception as e:
            QMessageBox.critical(
                parent_widget, 
                "System Error", 
                "Could not read the JSON file")
            return None

    elif file_path.endswith(".xlsx"):
        try:
            return pd.read_excel(file_path)
        except Exception as e:
            QMessageBox.critical(
                parent_widget, 
                "System Error", 
                f"Could not read EXCEL file")
            print(str(e))
            return None
