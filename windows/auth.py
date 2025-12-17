from interfaces.auth import Ui_Form
from PyQt6.QtWidgets import QMessageBox, QWidget
from database.base_dao import db
from windows.reservations import ReservationsWindow

class AuthWindow(Ui_Form, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.on_login_click)
        self.admin_window = None
    
    def on_login_click(self):
        email = self.login_edit.text().strip()
        password = self.password_edit.text().strip()

        # Проверка на пустые значения
        if not email or not password:
            QMessageBox.warning(self, "Ошибка", "Введите все поля")
        else:
            # Запрос в бд и проверка выходного значения
            user = db.auth(email, password)
            if user is None:
                 QMessageBox.warning(self, "Неверные данные", "Неправильный логин или пароль")
            else:
                QMessageBox.information(self, "Успех", "Вы авторизованы")
                role_id = user["user_role_id"]
                if role_id == 1:
                    self.admin_window = ReservationsWindow()
                    self.admin_window.show()
                    self.hide()



         
    


