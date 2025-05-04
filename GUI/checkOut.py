from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem
from db import connect
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtGui import QIntValidator

class CheckOut(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.layout = QHBoxLayout()
        self.stacked_widget = stacked_widget

        leftSideContainer = QWidget()
        leftSideLayout = QVBoxLayout()

        # Barcode
        barcodeLabel = QLabel()
        barcodeLabel.setText("Barcode: ")
        self.barcode = QLineEdit()
        self.barcode.setValidator(QIntValidator())
        self.barcode.setPlaceholderText("Enter Barcode...")
        self.barcode.returnPressed.connect(self.on_barcode_returned)
        leftSideLayout.addWidget(barcodeLabel)
        leftSideLayout.addWidget(self.barcode)

        # Error Label
        self.errorLabel = QLabel()
        self.errorLabel.setStyleSheet("color: red; font-weight: bold;")
        self.errorLabel.setAlignment(Qt.AlignCenter)
        self.errorLabel.setText("")
        leftSideLayout.addWidget(self.errorLabel)

        # Add a stretch to push buttons down
        leftSideLayout.addStretch()

        # Button container
        buttonContainer = QWidget()
        buttonLayout = QHBoxLayout()

        # Back button
        back = QPushButton("Back")
        back.clicked.connect(self.on_back_pressed)
        buttonLayout.addWidget(back, 1)

        # Check Out button
        checkOut = QPushButton("Check Out Items")
        checkOut.clicked.connect(self.on_check_out_pressed)
        buttonLayout.addWidget(checkOut, 3)

        # Add buttons to layout
        buttonContainer.setLayout(buttonLayout)
        leftSideLayout.addWidget(buttonContainer)

        # Add left side to the main layout -----------------------------
        leftSideContainer.setLayout(leftSideLayout)
        self.layout.addWidget(leftSideContainer, 2)

        # Right side layout
        rightContainer = QWidget()
        rightLayout = QVBoxLayout()

        # Item List
        self.itemList = QListWidget()
        self.itemList.setMaximumHeight(900)
        rightLayout.addWidget(self.itemList)

        # Total
        self.total = QLineEdit()
        self.total.setReadOnly(True)
        self.updateTotal()
        rightLayout.addWidget(self.total)

        #add the right side to the layout
        rightContainer.setLayout(rightLayout)

        #add the containers to the main layout
        self.layout.addWidget(rightContainer, 3)
        self.setLayout(self.layout)

    def on_back_pressed(self):
        self.itemList.clear()
        self.total.clear()
        self.stacked_widget.setCurrentIndex(1)
    
    def on_check_out_pressed(self):
        conn = connect()
        cursor = conn.cursor()

        # iterate through every item
        for i in range(self.itemList.count()):
            item = self.itemList.item(i)
            itemName = item.data(Qt.UserRole)

            # Subtract 1 from the quantity in the item table in the db
            cursor.execute("UPDATE item SET quantity = quantity - 1 WHERE name = %s", (itemName,))
        
        # Remove all of the items from the list
        self.itemList.clear()
        self.updateTotal()

        conn.commit()
        cursor.close()
        conn.close()
    
    def updateTotal(self):
        # Read the data from every itemList item
        sum = 0.0
        for i in range(self.itemList.count()):
            item = self.itemList.item(i)
            sum += float(item.data(Qt.UserRole + 1))

        self.total.setText(f"Total Cost: ${sum:.2f}")

    def on_barcode_returned(self):
        barcodeNum = int(self.barcode.text())

        # Query for item information
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name, cost FROM item WHERE barcode = %s", (barcodeNum, ))
        itemInfo = cursor.fetchone()

        # Check if barcode is correct
        if not itemInfo:
            self.errorLabel.setText("No Item With Barcode Exists.")
            return
        self.errorLabel.setText("")

        # Add itemInfo to the list
        item = QListWidgetItem(f"{itemInfo[0]:<30}${itemInfo[1]:>7.2f}")
        item.setData(Qt.UserRole, itemInfo[0])
        item.setData(Qt.UserRole + 1, itemInfo[1])
        self.itemList.addItem(item)

        # Update the total
        self.updateTotal()

        conn.commit()
        conn.close()
        cursor.close()
