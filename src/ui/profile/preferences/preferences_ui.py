from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QGroupBox,QLineEdit,QComboBox,QLabel,QPushButton,QWidget,QGridLayout,QColorDialog


class PreferencesUI(QWidget):
    change_preferred_language_request = pyqtSignal(str)
    change_preferred_theme_request = pyqtSignal(str)
    change_preferred_font_color_request = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.preferences_groupbox = QGroupBox()
        self.preferences_groupbox.setFixedSize(300,300)
        self.preferences_groupbox_layout = QGridLayout()
        self.preferences_groupbox.setLayout(self.preferences_groupbox_layout)
        self.layout.addWidget(self.preferences_groupbox,0,0)

        self.preferences_groupbox_layout.addWidget(QLabel("Language : "),0,0)
        self.language_preference_input = QComboBox()
        self.language_preference_input.addItem("English","en")
        self.language_preference_input.addItem("Deutsch","de")
        self.language_preference_input.addItem("Türkçe","tr")
        self.language_preference_input.currentIndexChanged.connect(self.save_preferred_language)
        self.preferences_groupbox_layout.addWidget(self.language_preference_input,0,1)
        
        self.preferences_groupbox_layout.addWidget(QLabel("Theme : "),1,0)
        self.theme_preference_input = QComboBox()
        self.theme_preference_input.addItem("Dark Theme","dark")
        self.theme_preference_input.addItem("Light Theme","light")
        self.theme_preference_input.currentIndexChanged.connect(self.save_preferred_theme)
        self.preferences_groupbox_layout.addWidget(self.theme_preference_input,1,1)

        self.preferences_groupbox_layout.addWidget(QLabel("Font Color : "),2,0)
        self.font_color_preference_input = QPushButton("Choose Font Color")
        self.font_color_preference_input.clicked.connect(self.save_preferred_font_color)
        self.preferences_groupbox_layout.addWidget(self.font_color_preference_input,2,1)

        self.output_space = QLineEdit()
        self.output_space.setReadOnly(True)
        self.output_space.setStyleSheet("""border : none;
                                        background-color :#2d333b; """)
        self.preferences_groupbox_layout.addWidget(self.output_space,3,0,1,2)

    # self.save_preferred_language --> MainUI --> AppManager --> DatabaseManager --> DataBase
    def save_preferred_language(self):
        new_prefered_language = self.language_preference_input.currentData()
        self.change_preferred_language_request.emit(new_prefered_language)
        self.output_space.setText("Preferred Language Changed")

    # self.save_preferred_theme --> MainUI --> AppManager --> DatabaseManager --> DataBase
    def save_preferred_theme(self):
        new_prefered_theme = self.theme_preference_input.currentData()
        self.change_preferred_theme_request.emit(new_prefered_theme)
        self.output_space.setText("Preferred Theme Changed")

    # self.save_preferred_font_color --> MainUI --> AppManager --> DatabaseManager --> DataBase
    def save_preferred_font_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            color_name = color.name()
            self.change_preferred_font_color_request.emit(color_name)
            self.output_space.setText("Preferred Font Color Changed")
        else:
            self.output_space.setText("Preferred Font Color Change Interrupted")
        




