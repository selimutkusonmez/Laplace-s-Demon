from PyQt6.QtWidgets import QMessageBox,QTextEdit

def load_text_data(file_path: str, partent_widget : QTextEdit):
    try:
        if not file_path.endswith((".csv",".txt")):
            return f"Error : Invalid supported file"
        
        with open(file_path, 'r', encoding="utf-8") as f:
            text = f.read().strip()

        text = text.replace("\n",",")
        raw_items = text.split(",")
        
        valid_numbers = []
        for item in raw_items:
            cleaned_item = item.strip()
            if cleaned_item:
                number = str(float(cleaned_item))
                valid_numbers.append(number)
                
        return ", ".join(valid_numbers)
    
    except ValueError:
        return f"Error : The file must contain only numbers separated by commas or newlines."
    
    except Exception as e:
        QMessageBox.critical(
            partent_widget,
            "System Error",
            f"Could not read the file: {str(e)}"
        )
        return None