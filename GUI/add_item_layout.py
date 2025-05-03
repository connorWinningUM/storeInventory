from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QLineEdit, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from GUI.searchSuppliersWidget import SupplierSearchWidget
from db import connect

class AddItemLayout(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.layout = QHBoxLayout()
        itemContainer = QWidget()
        itemContainer.setFixedWidth(500)
        itemLayout = QVBoxLayout()

        # Name
        nameContainer = QWidget()
        nameLayout = QHBoxLayout()
        nameLabel = QLabel()
        nameLabel.setText("Item Name: ")
        self.name = QLineEdit()
        self.name.setFixedWidth(300)
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(self.name)
        nameContainer.setLayout(nameLayout)
        itemLayout.addWidget(nameContainer)   

        # Category
        container = QWidget()
        layout = QHBoxLayout()
        label = QLabel()
        label.setText("Category: ")
        self.category = QComboBox()
        categoryList = [
            "General",
            "Beverages",
            "Household",
            "Personal Care",
            "Baby and Childcare",
            "Pet Supplies",
            "Hardware and Tools",
            "Electronics",
            "Clothing",
            "Groceries",
            "Stationary"
        ]
        self.category.addItems(categoryList)
        self.category.setFixedWidth(300)
        layout.addWidget(label)
        layout.addWidget(self.category)
        container.setLayout(layout)
        itemLayout.addWidget(container) 

        # Quantity
        container = QWidget()
        layout = QHBoxLayout()
        label = QLabel()
        label.setText("Quantity: ")
        self.quantity = QLineEdit()
        self.quantity.setValidator(QIntValidator())
        self.quantity.setFixedWidth(300)
        layout.addWidget(label)
        layout.addWidget(self.quantity)
        container.setLayout(layout)
        itemLayout.addWidget(container)    

        # Cost
        container = QWidget()
        layout = QHBoxLayout()
        label = QLabel()
        label.setText("Cost: ")
        self.cost = QLineEdit()
        double_validator = QDoubleValidator(0.00, 999999.99, 2)     # validates that it is 2 decimal places
        double_validator.setNotation(QDoubleValidator.StandardNotation)
        self.cost.setValidator(double_validator)
        self.cost.setFixedWidth(300)
        layout.addWidget(label)
        layout.addWidget(self.cost)
        container.setLayout(layout)
        itemLayout.addWidget(container) 

        # Description
        container = QWidget()
        layout = QHBoxLayout()
        label = QLabel()
        label.setText("Description: ")
        self.description = QLineEdit()
        self.description.setFixedWidth(300)
        self.description.setFixedHeight(300)
        layout.addWidget(label, alignment=Qt.AlignTop)
        layout.addWidget(self.description)
        container.setLayout(layout)
        itemLayout.addWidget(container) 

        # Barcode
        container = QWidget()
        layout = QHBoxLayout()
        label = QLabel()
        label.setText("Barcode: ")
        self.barcode = QLineEdit()
        self.barcode.setValidator(QIntValidator())
        self.barcode.setFixedWidth(300)
        layout.addWidget(label)
        layout.addWidget(self.barcode)
        container.setLayout(layout)
        itemLayout.addWidget(container) 

        # error label
        self.errorLabel = QLabel()
        self.errorLabel.setText("")
        self.errorLabel.setStyleSheet("color: red; font-weight: bold;")
        itemLayout.addWidget(self.errorLabel) 

        # submit button
        container = QWidget()
        layout = QHBoxLayout()
        submitButton = QPushButton("Submit")
        submitButton.clicked.connect(self.on_submit)
        backButton = QPushButton("Back")
        backButton.clicked.connect(self.on_back_pressed)
        layout.addWidget(backButton)
        layout.addWidget(submitButton)
        container.setLayout(layout)
        itemLayout.addStretch()                 # this will push everything apart in itemLayout at this point
        itemLayout.addWidget(container) 


        #add the item side to the layout
        itemContainer.setLayout(itemLayout)
        self.layout.addWidget(itemContainer)

        # now the supplier side
        self.supplier = SupplierSearchWidget()
        self.layout.addWidget(self.supplier)


        self.setLayout(self.layout)

    def on_submit(self):
        # check if any feilds are empty
        if self.name.text() == "":
            self.errorLabel.setText("No Item Name Specified")
            return
        if self.quantity.text() == "":
            self.errorLabel.setText("No Quantity Specified. If there is no current Quantity input 0.")
            return
        if self.cost.text() == "":
            self.errorLabel.setText("No Cost Specified")
            return
        if self.description.text() == "":
            self.errorLabel.setText("No Description Specified")
            return
        if self.barcode.text() == "":
            self.errorLabel.setText("No Barcode")
            return
        if self.supplier.get_selected_supplier_id() == "":
            self.errorLabel.setText("Select A Supplier")
            return

        conn = connect()
        cursor = conn.cursor()

        #check if name is already taken
        cursor.execute("SELECT * FROM item_suppliers WHERE item_name = %s", (self.name.text(),))
        if cursor.fetchone():
            self.errorLabel.setText("Item Name already Taken")
            return
        
        #check if barcode is already taken
        cursor.execute("SELECT * FROM item_suppliers WHERE barcode = %s", (int(self.barcode.text()),))
        if cursor.fetchone():
            self.errorLabel.setText("Barcode Already Allocated to Another Item")

        #query for user location from username
        cursor.execute("SELECT store_num FROM employee WHERE username = %s", (self.username,))
        store_num = cursor.fetchone()

        #insert item into the database
        supplier_id = self.supplier.get_selected_supplier_id()
        barcode = int(self.barcode.text())
        params = []
        params.append(barcode)
        params.append(self.name.text())
        params.append(int(self.quantity.text()))
        params.append(self.description.text())
        params.append(self.category.currentData())
        params.append(float(self.cost.text()))
        params.append(store_num)
        cursor.execute("INSERT INTO item (barcode, name, quantity, description, category, cost, store_num) VALUES (%s, %s, %s, %s, %s, %s, %s)", params)
        cursor.execute("INSERT INTO supplies (supplier_id, barcode) VALUES (%s, %s)", (supplier_id, barcode))
        conn.commit()
        self.stacked_widget.setCurrentIndex(1)
        cursor.close()
        conn.close()
        
    
    def on_back_pressed(self):
        self.stacked_widget.setCurrentIndex(1)

    def pass_username(self, username):
        self.username = username