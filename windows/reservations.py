from typing import Any

import pymysql
from interfaces.reservations import Ui_Form
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QWidget, QApplication
from database.base_dao import db
from windows.add_reservation import AddDialog
from windows.edit_reservation import EditDialog

class ReservationsWindow(Ui_Form, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        data = db.get_reservations_info()
        self.load_data(data)
        self.filter_button.clicked.connect(self.filter_reservations)
        self.show_all_button.clicked.connect(lambda: self.load_data(db.get_reservations_info()))
        self.add_button.clicked.connect(self.open_add_dialog)
        self.delete_button.clicked.connect(self.delete_booking)
        self.update_button.clicked.connect(self.open_edit_dialog)
    
    def delete_booking(self):
        row = self.tableWidget.currentRow() # -1

        if row == -1:
             QMessageBox.warning(self, "Не выбрана запись", "Для удаления выберите интересующую вас запись")
        else:
            booking_id = int(self.tableWidget.item(row, 0).text())
            db.delete("bookings", booking_id)
            bookings = db.get_reservations_info()
            self.load_data(bookings)


    def open_add_dialog(self):
        self.add_dialog = AddDialog(parent=self)
        self.add_dialog.accepted.connect(self.insert_booking)
        self.add_dialog.exec()
    
    def open_edit_dialog(self):
        self.edit_dialog = EditDialog(self)
        self.edit_dialog.accepted.connect(self.update_booking)
        if self.tableWidget.currentRow() != 1:
            self.edit_dialog.exec()
        else:
             QMessageBox.warning(self, "Не выбрана запись", "Для редактирования выберите интересующую вас запись")
    
    def insert_booking(self):
        client_id = self.add_dialog.client_combobox.currentData()
        room_id = self.add_dialog.room_combobox.currentData()
        start_date = self.add_dialog.check_in_date1.date().toString("yyyy-MM-dd")
        end_date = self.add_dialog.check_out_date.date().toString("yyyy-MM-dd")

        try:
            db.insert_booking(client_id, room_id, start_date, end_date)
            bookings = db.get_reservations_info()
            self.load_data(bookings)
        except pymysql.ProgrammingError as e:
            print(e)
    
    def update_booking(self):
        client_id = self.edit_dialog.client_combobox.currentData()
        room_id = self.edit_dialog.room_combobox.currentData()
        start_date = self.edit_dialog.check_in_date_2.date().toString("yyyy-MM-dd")
        end_date = self.edit_dialog.check_out_date.date().toString("yyyy-MM-dd")
        booking_id = int(self.tableWidget.item(self.tableWidget.currentRow(), 0).text())
        db.update_booking(booking_id, client_id, room_id, start_date,end_date)
        bookings = db.get_reservations_info()
        self.load_data(bookings)


    def filter_reservations(self):
        start_date = self.start_date_edit.date()
        end_date = self.end_date_edit.date()
        
        if start_date < end_date:
            # Фильтровать
            filtered_reservations = db.get_reservations_info_filtered(start_date, end_date)
            self.load_data(filtered_reservations)
            pass
        else:
            QMessageBox.warning(self, "Неправильный период", "Начало периода должно быть раньше конца периода")

    
    def load_data(self, data: list[dict[str, Any]]):# Список строк БД 
        # Каждая запись представлена словарем
        self.tableWidget.setRowCount(len(data))

        # Первый способ: 1 цикл for
        # for row_idx, reservartion in enumerate(reservations): # [(0, reservation1), (1, reservation2)]
        #     self.tableWidget.setItem(row_idx, 0, QTableWidgetItem(str(reservartion["id"])))
        #     self.tableWidget.setItem(row_idx, 1, QTableWidgetItem(str(reservartion["fio"])))
        #     self.tableWidget.setItem(row_idx, 2, QTableWidgetItem(str(reservartion["room_number"])))
        #     self.tableWidget.setItem(row_idx, 3, QTableWidgetItem(str(reservartion["room_type"])))
        #     self.tableWidget.setItem(row_idx, 4, QTableWidgetItem(str(reservartion["start_date"])))
        #     self.tableWidget.setItem(row_idx, 5, QTableWidgetItem(str(reservartion["end_date"])))
        #     self.tableWidget.setItem(row_idx, 6, QTableWidgetItem(str(reservartion["status_name"])))
        #     self.tableWidget.setItem(row_idx, 7, QTableWidgetItem(str(reservartion["total_price"])))
        
        # Второй способ: через два цикла for
        for row_idx, reservartion in enumerate(data):
            for col_idx, col in enumerate(reservartion):
                self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(reservartion.get(col)))) # {"id": 1, }
        

if __name__ == "__main__":
    app = QApplication([])
    window = ReservationsWindow()
    window.show()
    app.exec()






            

        


    

        