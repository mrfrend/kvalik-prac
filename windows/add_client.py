from interfaces.add_client import Ui_Dialog
from PyQt6.QtWidgets import QDialog, QMessageBox
from database.base_dao import db

class AddClientDialog(Ui_Dialog, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.add_button.clicked.connect(self.accept)
    
    def validate_data(self):
        last_name = self.last_name_edit.text()
        first_name = self.nameLineEdit.text()
        phone_number = self.phoneLineEdit.text()

        if not last_name or not first_name:
            QMessageBox.warning(self, "Пустые поля", "Введите обязательные данные: Фамилия и Имя")
            return False
        if phone_number and not (len(phone_number) == 12 and phone_number.startswith("+7") and phone_number[1:].isdigit()):
            QMessageBox.warning(self, "Неправильный формат", "Введите номер телефона соответствующего формата: +7XXXXXXXXXX")
            return False
        
        return True

        # Check phone number

    
    def accept(self):
        last_name = self.last_name_edit.text()
        first_name = self.nameLineEdit.text()
        middle_name = self.middleNameLineEdit.text()
        passport_series = self.passportSeriesSpinbox.value()
        passport_number = self.passportSeriesSpinbox_2.value()
        phone_number = self.phoneLineEdit.text()
        preferences = self.preferencesLineEdit.text()

        if self.validate_data():
            super().accept()

    


