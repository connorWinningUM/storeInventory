from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton

class InventoryLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # Inventory list (Placeholder)
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        # Refresh button
        refresh_btn = QPushButton("Refresh Inventory")
        self.layout.addWidget(refresh_btn)

        # Add Item button
        add_item_btn = QPushButton("Go to Add Item")
        self.layout.addWidget(add_item_btn)

        self.setLayout(self.layout)
