from PyQt6.QtWidgets import QDialog
from PyQt6 import uic
from database.base_dao import db

class BaseDialog(QDialog):
    def __init__(self, path_to_ui: str, parent=None) -> None:
        super().__init__(parent)
        uic.loadUi(path_to_ui, self)


    
