from interfaces.add_client import Ui_Dialog
from PyQt6.QtWidgets import QDialog, QMessageBox
from database.base_dao import db

class EditClientDialog(Ui_Dialog, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.add_button.setText("Изменить")
        self.title.setText("Изменить данные клиента")
        self.add_button.clicked.connect(self.accept)
        self.client_id = self.parent().buttonGroup.checkedId()
        self.set_data()
    
    def set_data(self):
        client = db.get_by_id("guests", self.client_id)
        self.last_name_edit.setText(client["last_name"])
        self.nameLineEdit.setText(client["first_name"])
        self.middleNameLineEdit.setText(client["middle_name"])
        self.passportSeriesSpinbox.setValue(int(client["passport_series"]))
        self.passportSeriesSpinbox_2.setValue(int(client["passport_number"]))
        self.phoneLineEdit.setText(client["phone"])
        self.preferencesLineEdit.setText(client["preferences"])
    
    def validate_data(self):
        phone_number = self.phoneLineEdit.text()
        last_name = self.last_name_edit.text()
        first_name = self.nameLineEdit.text()
        middle_name = self.middleNameLineEdit.text()
        passport_series = self.passportSeriesSpinbox.value()
        passport_number = self.passportSeriesSpinbox_2.value()
        preferences = self.preferencesLineEdit.text()

        if not all([phone_number, last_name, first_name, middle_name, preferences]):
            QMessageBox.warning(self, "Пустые поля", "Введите обязательные данные: Фамилия, Имя и Номер телефона")
            return False
        
        if phone_number and not (len(phone_number) == 12 and phone_number.startswith("+7") and phone_number[1:].isdigit()):
            QMessageBox.warning(self, "Неправильный формат", "Введите номер телефона соответствующего формата: +7XXXXXXXXXX")
            return False
        
        return True

        # Check phone number

    
    def accept(self):
        if self.validate_data():
            super().accept()

    


