from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QGroupBox,QLineEdit,QComboBox,QLabel,QPushButton,QWidget,QGridLayout,QColorDialog,QCheckBox
from PyQt6.QtGui import QColor


class PreferencesUI(QWidget):
    preferred_language_update_requested = pyqtSignal(str)
    preferred_theme_update_requested = pyqtSignal(str)
    preferred_font_color_update_requested = pyqtSignal(str)
    remember_me_state_update_requested = pyqtSignal(bool)
    
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
        self.language_preference_input.currentIndexChanged.connect(self.request_preferred_language_update)
        self.preferences_groupbox_layout.addWidget(self.language_preference_input,0,1)
        
        self.preferences_groupbox_layout.addWidget(QLabel("Theme : "),1,0)
        self.theme_preference_input = QComboBox()
        self.theme_preference_input.addItem("Dark Theme","dark")
        self.theme_preference_input.addItem("Light Theme","light")
        self.theme_preference_input.currentIndexChanged.connect(self.request_preferred_theme_update)
        self.preferences_groupbox_layout.addWidget(self.theme_preference_input,1,1)

        self.preferences_groupbox_layout.addWidget(QLabel("Font Color : "),2,0)
        self.font_color_preference_input = QPushButton("Choose Font Color")
        self.font_color_preference_input.clicked.connect(self.request_preferred_font_color_update)
        self.preferences_groupbox_layout.addWidget(self.font_color_preference_input,2,1)
        
        self.preferences_groupbox_layout.addWidget(QLabel("Remember Me : "),3,0)

        self.remember_me_checkbox = QCheckBox("Remember Me")
        self.remember_me_checkbox.checkStateChanged.connect(self.request_remember_me_state_update)
        self.preferences_groupbox_layout.addWidget(self.remember_me_checkbox,3,1)

        self.output_space = QLineEdit()
        self.output_space.setReadOnly(True)
        self.output_space.setStyleSheet("""border : none;
                                        """)
        self.preferences_groupbox_layout.addWidget(self.output_space,4,0,1,2)

    # PreferencesUI.request_update_preferred_language.change_preferred_language_request --> MainUI.update_preferred_language_requested --> AppManager.handle_preferred_language_change --> DatabaseManager.update_preferred_language
    def request_preferred_language_update(self):
        new_prefered_language = self.language_preference_input.currentData()
        self.preferred_language_update_requested.emit(new_prefered_language)
        self.output_space.setText("Preferred Language Updated")

    # sePreferencesUIlf.request_update_preferred_theme.update_preferred_theme_requested --> MainUI.update_preferred_theme_requested --> AppManager.handle_preferred_theme_change --> DatabaseManager.update_preferred_theme
    def request_preferred_theme_update(self):
        new_prefered_theme = self.theme_preference_input.currentData()
        self.preferred_theme_update_requested.emit(new_prefered_theme)
        self.output_space.setText("Preferred Theme Updated")

    # PreferencesUI.request_update_preferred_font_color.update_preferred_font_color_requested --> MainUI.update_preferred_font_color_requested --> AppManager.handle_preffered_font_color_change --> DatabaseManager.update_preferred_font_color
    def request_preferred_font_color_update(self):
        color = QColorDialog.getColor(self.current_preferred_font_color)
        if color.isValid():
            color_name = color.name()
            self.current_preferred_font_color = color
            self.preferred_font_color_update_requested.emit(color_name)
            self.output_space.setText("Preferred Font Color Updated")
        else:
            self.output_space.setText("Preferred Font Color Update Interrupted")
    
    def request_remember_me_state_update(self):
        new_remember_state = self.remember_me_checkbox.isChecked()
        self.remember_me_state_update_requested.emit(new_remember_state)

    def set_preferences(self,current_user_preferences : list,remember_me_state : bool):
        current_preferred_language = current_user_preferences[0]
        if current_preferred_language == "en":
            current_preferred_language = "English"
        elif current_preferred_language == "de":
            current_preferred_language = "Deutsch"
        elif current_preferred_language == "tr":
            current_preferred_language = "Türkçe"
        self.language_preference_input.setCurrentText(current_preferred_language)

        current_preferred_theme = current_user_preferences[1]
        if current_preferred_theme == "dark":
            current_preferred_theme = "Dark Theme"
        elif current_preferred_theme == "light":
            current_preferred_theme = "Light Theme"
        self.theme_preference_input.setCurrentText(current_preferred_theme)

        self.current_preferred_font_color = QColor(current_user_preferences[2])

        if remember_me_state:
            self.remember_me_checkbox.setChecked(True)
        else:
            self.remember_me_checkbox.setChecked(False)
        




