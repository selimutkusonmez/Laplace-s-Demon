import pandas as pd
from PyQt6.QtWidgets import QMessageBox,QTableWidget

def load_table_data(file_path : str, parent_widget : QTableWidget) -> pd.DataFrame:

    #We accept only csv,tsv,txt,json and xlsx

    #If file extension in (csv,tsv,txt)
    if file_path.endswith((".csv",".tsv",".txt")):
        try:
            #Return data as DataFrame
            return pd.read_csv(file_path,sep=None,engine="python")
        
        except Exception as e:
            QMessageBox.critical(
                parent_widget, 
                "System Error", 
                f"Could not read the file")
            
            return None
        

    #If file is a json file   
    elif file_path.endswith(".json"):
        try:
            #Return data as DataFrame
            df = pd.read_json(file_path)

            #We don't support Nested JSON
            for column in df.columns:
                if any(isinstance(val,(dict,list)) for val in df[column]):
                    raise ValueError
                
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
        

    #If file is a Excel file
    elif file_path.endswith(".xlsx"):
        try:
            #Return data as DataFrame
            return pd.read_excel(file_path)
        
        except Exception as e:
            QMessageBox.war(
                parent_widget, 
                "System Error", 
                f"Could not read EXCEL file")
            print(str(e))
            return None
