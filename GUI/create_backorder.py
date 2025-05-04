from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel, QHBoxLayout, QVBoxLayout,  QDateEdit
from PyQt5.QtCore import Qt, QDate
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

    def pass_username(self, username):
        self.username = username

    def on_create_pressed(self):
        self.barcode
        self.quantity
        date = f"{self.completeDate.date().year()}-{self.completeDate.date().month()}-{self.completeDate.date().day()}"
        supplierId = self.supplier.get_selected_supplier_id()

        startDate = f"{QDate.currentDate().year()}-{QDate.currentDate().month()}-{QDate.currentDate().day()}"
        
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT ssn, store_num FROM employee WHERE username = %s", (self.username, ))
        employee = cursor.fetchone()
        employeeSSN = employee[0]
        storeNum = employee[1]

        cursor.execute("SELECT MAX(order_num) FROM backorder")
        orderNum = cursor.fetchone()[0] + 1

        cursor.execute("""
        INSERT INTO backorder (order_num, complete_date, start_date, quantity, employee_ssn, barcode, supplier_id, store_num) VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (orderNum, date, startDate, int(self.quantity.text()), employeeSSN, int(self.barcode.text()), supplierId, storeNum))

        conn.commit()
        cursor.close()
        conn.close()

        self.barcode.clear()
        self.quantity.clear()
        return