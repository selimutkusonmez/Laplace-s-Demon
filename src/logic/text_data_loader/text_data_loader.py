from PyQt6.QtWidgets import QMessageBox,QTextEdit

def load_text_data(file_path: str, partent_widget : QTextEdit):

    #We accept only csv,tsv,txt

    try:
        
        #If file extension not in (csv,txt,tsv)
        if not file_path.endswith((".csv",".txt",".tsv")):
            QMessageBox.warning(
                partent_widget,
                "File Error",
                "Supported files only (csv,txt,tsv)"
            )
            return None 
        
        #Read the file
        with open(file_path, 'r', encoding="utf-8") as f:
            text = f.read().strip()

        #Replace newlines with comma
        text = text.replace("\n",",")
        #Split data by comma
        raw_items = text.split(",")
        
        #Float data
        valid_numbers = []
        for item in raw_items:
            cleaned_item = item.strip()
            if cleaned_item:
                number = str(float(cleaned_item))
                valid_numbers.append(number)
                
        #Return string data joined with comma
        return ", ".join(valid_numbers)
    
    #We dont support text data
    except ValueError:
        QMessageBox.warning(
            partent_widget,
            "Data Error",
            "The file must contain only numbers separated by commas or newlines."
        )
        return None 
    
    except Exception as e:
        QMessageBox.critical(
            partent_widget,
            "System Error",
            f"Could not read the file: {str(e)}"
        )
        return None