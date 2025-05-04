from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel, QHBoxLayout, QVBoxLayout,  QDateEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from db import connect
from GUI.searchSuppliersWidget import SupplierSearchWidget

class CreateBackorder(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.layout = QHBoxLayout()
        self.stacked_widget = stacked_widget

        # Left Container
        leftSide = QWidget()
        leftLayout = QVBoxLayout()

        # Barcode
        container = QWidget()
        layout = QHBoxLayout()
        barcodeLabel = QLabel()
        barcodeLabel.setText("Item Barcode: ")
        layout.addWidget(barcodeLabel, alignment=Qt.AlignLeft)
        self.barcode = QLineEdit()
        self.barcode.setValidator(QIntValidator())
        layout.addWidget(self.barcode, alignment=Qt.AlignRight)
        container.setLayout(layout)
        leftLayout.addWidget(container)

        # Quantity
        container = QWidget()
        layout = QHBoxLayout()
        quantityLabel = QLabel("Quantity: ")
        layout.addWidget(quantityLabel, alignment=Qt.AlignLeft)
        self.quantity = QLineEdit()
        self.quantity.setValidator(QIntValidator())
        layout.addWidget(self.quantity, alignment=Qt.AlignRight)
        container.setLayout(layout)
        leftLayout.addWidget(container)

        # Complete Date(select date)
        container = QWidget()
        layout = QHBoxLayout()
        dateLabel = QLabel("Order Complete Date: ")
        self.completeDate = QDateEdit()
        self.completeDate.setDisplayFormat("MM/dd/yyyy")
        self.completeDate.setCalendarPopup(True)
        layout.addWidget(dateLabel)
        layout.addWidget(self.completeDate)
        container.setLayout(layout)
        leftLayout.addWidget(container)

        # Error Label
        self.errorLabel = QLabel()
        self.errorLabel.setStyleSheet("color: red; font-weight: bold;")
        self.errorLabel.setAlignment(Qt.AlignCenter)
        self.errorLabel.setText("")
        leftLayout.addWidget(self.errorLabel)

        # Stretch
        leftLayout.addStretch()

        # Buttons ------------
        buttons = QWidget()
        buttonLayout = QHBoxLayout()

        # Back
        backBtn = QPushButton("Back")
        backBtn.clicked.connect(self.on_back_pressed)
        buttonLayout.addWidget(backBtn, 1)

        # Create backOrder
        createBtn = QPushButton("Create Backorder")
        createBtn.clicked.connect(self.on_create_pressed)
        buttonLayout.addWidget(createBtn, 3)
        buttons.setLayout(buttonLayout)
        leftLayout.addWidget(buttons)

        leftSide.setLayout(leftLayout)
        self.layout.addWidget(leftSide)

        # Right side (supplier widget)
        self.supplier = SupplierSearchWidget()
        self.layout.addWidget(self.supplier)

        self.setLayout(self.layout)

    def on_back_pressed(self):
        self.stacked_widget.setCurrentIndex(1)

    def on_create_pressed(self):
        return