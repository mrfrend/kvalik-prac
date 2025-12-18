from PyQt6.QtWidgets import QDialog, QMessageBox, QWidget, QApplication, QRadioButton, QButtonGroup
from database.base_dao import db
from interfaces.client import Ui_Form
from windows.add_client import AddClientDialog
from windows.edit_client import EditClientDialog

class ClientWindow(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.add_button.clicked.connect(self.open_add_dialog)
        self.load_data()
        self.delete_button.clicked.connect(self.delete_client)
        self.update_button.clicked.connect(self.open_edit_dialog)
    
    def open_add_dialog(self):
        self.add_dialog = AddClientDialog(self)
        self.add_dialog.accepted.connect(self.add_client)
        self.add_dialog.exec()
    
    def add_client(self):
        last_name = self.add_dialog.last_name_edit.text()
        first_name = self.add_dialog.nameLineEdit.text()
        middle_name = self.add_dialog.middleNameLineEdit.text()
        passport_series = self.add_dialog.passportSeriesSpinbox.value()
        passport_number = self.add_dialog.passportSeriesSpinbox_2.value()
        phone_number = self.add_dialog.phoneLineEdit.text()
        preferences = self.add_dialog.preferencesLineEdit.text()

        db.insert_client(last_name, first_name, middle_name, passport_series, passport_number, phone_number, preferences)
        self.load_data()
    
    def delete_client(self):
        client_id = self.buttonGroup.checkedId()
        if client_id == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите клиента для удаления")
        else:
            db.delete("guests", client_id)
            self.load_data()
    
    def open_edit_dialog(self):
        self.edit_dialog = EditClientDialog(self)
        if self.buttonGroup.checkedId() == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите клиента для редактирования")
        else:
            self.edit_dialog.accepted.connect(self.update_client)
            self.edit_dialog.exec()
    
    def update_client(self):
        db.update_client(self.edit_dialog.client_id, self.edit_dialog.nameLineEdit.text(), self.edit_dialog.last_name_edit.text(), self.edit_dialog.middleNameLineEdit.text(), self.edit_dialog.passportSeriesSpinbox.value(), self.edit_dialog.passportSeriesSpinbox_2.value(), self.edit_dialog.phoneLineEdit.text(), self.edit_dialog.preferencesLineEdit.text())
        self.load_data()

    def clean_clients(self):
        layout = self.verticalLayout_3
        while layout.count():
            item = layout.takeAt(0)

            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        
    def load_data(self):
        self.clean_clients()
        clients = db.get_all("guests")

        self.buttonGroup = QButtonGroup()
        self.buttonGroup.setExclusive(True)

        for client in clients:
            formatted_text = f"{client["last_name"]} {client["first_name"]} {client["middle_name"]} | {client["passport_series"]} | {client["passport_number"]} | {client["preferences"]}"
            client_radio: QRadioButton = QRadioButton(formatted_text)
            self.buttonGroup.addButton(client_radio, client["id"])
            self.verticalLayout_3.addWidget(client_radio)
    


if __name__ == "__main__":
    app = QApplication([])
    window = ClientWindow()
    window.show()
    app.exec()
