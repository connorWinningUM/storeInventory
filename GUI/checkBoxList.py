from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt
import sys

class CheckBoxListWidget(QWidget):
    def __init__(self, items):
        super().__init__()
        layout = QVBoxLayout()
        self.list_widget = QListWidget()

        for item_text in items:
            item = QListWidgetItem(item_text)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.list_widget.addItem(item)

        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def get_checked_items(self):
        checked = []
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            if item.checkState() == Qt.Checked:
                checked.append(item.text())
        return checked