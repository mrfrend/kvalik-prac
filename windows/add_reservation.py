from interfaces.add_reservation import Ui_Dialog
from PyQt6.QtWidgets import QDialog, QMessageBox
from database.base_dao import db

class AddDialog(Ui_Dialog, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.load_clients()
        self.load_rooms()
        self.add_button.clicked.connect(self.validate_data)

    
    def load_clients(self):
        clients = db.get_all("guests")
        for client in clients:
            fio = f"{client['last_name']} {client["first_name"]} {client["middle_name"]}"
            self.client_combobox.addItem(fio, client['id'])
    
    def validate_data(self):
        check_in = self.check_in_date1.date()
        check_out = self.check_out_date.date()
        if check_in < check_out:
            self.accept() # Все чики пуки, закрывается
        else:
            QMessageBox.warning(self, "Неправильные даты", "Дата въезда должна быть раньше даты выезда")

    
    
    def load_rooms(self):
        rooms = db.get_all("rooms")
        rooms = [room for room in rooms if room["status_id"] == 1]
        for room in rooms:
            self.room_combobox.addItem(room["room_number"], room['id'])
