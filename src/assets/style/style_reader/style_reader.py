import os
from config import STYLE_PATH

def read_style(current_theme):
    if current_theme == "dark":
        file_name = "main_ui_dark_theme.qss"
    else:
        file_name = "main_ui_light_theme.qss"

    file_path = os.path.join(STYLE_PATH,file_name)
    
    with open(file_path,"r") as f:
        qss_content = f.read()

    return qss_content
    
