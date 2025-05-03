from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

class AdminSettingsLayout(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.layout = QVBoxLayout()

        # Admin settings options (Placeholder)
        self.layout.addWidget(QPushButton("Admin Settings Form"))

        # Back button
        back_btn = QPushButton("Back to Inventory")
        self.layout.addWidget(back_btn)

        self.setLayout(self.layout)
