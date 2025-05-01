from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

class AddItemLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # Add Item form (Placeholder)
        self.layout.addWidget(QPushButton("Form to Add Item"))

        # Back button
        back_btn = QPushButton("Back to Inventory")
        self.layout.addWidget(back_btn)

        self.setLayout(self.layout)
