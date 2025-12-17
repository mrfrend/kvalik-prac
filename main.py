from PyQt6.QtWidgets import QApplication
from windows.auth import AuthWindow

app = QApplication([])
window = AuthWindow()
window.show()
app.exec()