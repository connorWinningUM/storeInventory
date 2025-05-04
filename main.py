import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QListWidget, QPushButton, QMessageBox, 
    QStackedWidget, QFormLayout, QLineEdit
)
from db import connect
from GUI.login_layout import LoginLayout
from GUI.inventory_layout import InventoryLayout
from GUI.add_item_layout import AddItemLayout
from GUI.manageAccounts import ManageAccounts
from GUI.create_account import CreateAccount
from GUI.statistics import InventoryStatistics
from GUI.checkOut import CheckOut

class InventoryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Store Inventory")
        self.setGeometry(100, 100, 600, 400)

        # stacked_widget holds layouts in it
        self.stacked_widget = QStackedWidget()
        self.main_layout = QVBoxLayout()

        # create all of the layouts for the window
        self.login_layout = LoginLayout(self.stacked_widget)
        self.inventory_layout = InventoryLayout(self.stacked_widget)
        self.add_item_layout = AddItemLayout(self.stacked_widget)
        self.manageAccounts = ManageAccounts(self.stacked_widget)
        self.create_account_layout = CreateAccount(self.stacked_widget)
        self.inventory_stats = InventoryStatistics(self.stacked_widget)
        self.check_out_item = CheckOut(self.stacked_widget)

        # store all of the layouts in the stacked widget object (seperate screens/windows)
        self.stacked_widget.addWidget(self.login_layout)            # index: 0
        self.stacked_widget.addWidget(self.inventory_layout)        # index: 1
        self.stacked_widget.addWidget(self.add_item_layout)         # index: 2
        self.stacked_widget.addWidget(self.manageAccounts)          # index: 3
        self.stacked_widget.addWidget(self.create_account_layout)   # index: 4
        self.stacked_widget.addWidget(self.inventory_stats)         # index: 5
        self.stacked_widget.addWidget(self.check_out_item)          # index: 6

        # set initial screen
        self.stacked_widget.setCurrentIndex(0)

        # set the stacked widget as main_layout
        self.main_layout.addWidget(self.stacked_widget)
        self.setLayout(self.main_layout)



if __name__ == "__main__":
    app = QApplication([])
    window = InventoryApp()
    window.show()
    app.exec_()