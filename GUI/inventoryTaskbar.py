from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox,
    QPushButton, QListWidget, QLabel,
)
from db import connect
from PyQt5.QtCore import Qt
from GUI.checkBoxList import CheckBoxListWidget
from PyQt5.QtGui import QDoubleValidator, QIntValidator

class inventoryTaskbar(QWidget):
    def __init__(self, on_search):
        super().__init__()

        self.layout = QVBoxLayout()

        # store select
        storeSelectLabel = QLabel("Select Store: ")
        self.layout.addWidget(storeSelectLabel)
        self.storeSelect = QComboBox()
        self.updateStores()

        # Search By
        self.searchBy = QComboBox()
        searchCategories = [
            ("Barcode", "barcode"), 
            ("Name", "item_name"), 
            ("Item Description", "description"), 
            ("Supplier Name", "supplier_name"), 
            ("Supplier ID", "supplier_id")
        ]
        for display_text, data_value in searchCategories:
            self.searchBy.addItem(display_text, data_value)

        # search bar
        searchBarContainer = QWidget()
        searchBarLayout = QHBoxLayout()
        self.search_bar_input = QLineEdit()
        self.search_bar_input.setPlaceholderText("Barcode, Name, Supplier or Keywords")
        searchButton = QPushButton("Search")
        searchButton.clicked.connect(on_search)
        searchBarLayout.addWidget(self.searchBy, stretch=2)
        searchBarLayout.addWidget(self.search_bar_input, stretch=10)
        searchBarLayout.addWidget(searchButton, stretch=1)
        searchBarContainer.setLayout(searchBarLayout)
        self.layout.addWidget(searchBarContainer)

        # Sort By
        sortByContainer = QWidget()
        sortByLayout = QHBoxLayout()
        sortByLabel = QLabel("Sort By: ")
        self.sortByList = QComboBox()
        sortCategories = [
            ("Name", "item_name"),
            ("Supplier", "supplier_id"),
            ("Quantity", "quantity"),
            ("Backorder Count", "backorder_count"),
            ("Cost", "cost")
        ]
        for display_text, data_value in sortCategories:
            self.sortByList.addItem(display_text, data_value)
        sortByLayout.addWidget(sortByLabel)
        sortByLayout.addWidget(self.sortByList)
        sortByContainer.setLayout(sortByLayout)
        self.layout.addWidget(sortByContainer, alignment=Qt.AlignLeft)

        # Quantity Range
        quantityContainer = QWidget()
        quantityLayout = QHBoxLayout()
        quantityLabel = QLabel("Quantity: ")
        quantityLayout.addWidget(quantityLabel)
        quantityLabel1 = QLabel("From ")
        self.quantityMin = QLineEdit()
        self.quantityMin.setPlaceholderText("Min")
        self.quantityMin.setValidator(QIntValidator())
        quantityLabel2 = QLabel(" to ")
        self.quantityMax = QLineEdit()
        self.quantityMax.setPlaceholderText("Max")
        self.quantityMax.setValidator(QIntValidator())
        quantityLayout.addWidget(quantityLabel1)
        quantityLayout.addWidget(self.quantityMin)
        quantityLayout.addWidget(quantityLabel2)
        quantityLayout.addWidget(self.quantityMax)
        quantityContainer.setLayout(quantityLayout)
        self.layout.addWidget(quantityContainer)

        # Cost
        costContainer = QWidget()
        costLayout = QHBoxLayout()
        costLabel = QLabel("Cost: ")
        costLayout.addWidget(costLabel)
        costLabel1 = QLabel("From ")
        self.costMin = QLineEdit()
        self.costMin.setPlaceholderText("Min")
        self.costMin.setValidator(QDoubleValidator())
        costLabel2 = QLabel(" to ")
        self.costMax = QLineEdit()
        self.costMax.setPlaceholderText("Max")
        self.costMax.setValidator(QDoubleValidator())
        costLayout.addWidget(costLabel1)
        costLayout.addWidget(self.costMin)
        costLayout.addWidget(costLabel2)
        costLayout.addWidget(self.costMax)
        costContainer.setLayout(costLayout)
        self.layout.addWidget(costContainer)

        # Supplier
        supplierContainer = QWidget()
        supplierLayout = QHBoxLayout()
        supplierLabel = QLabel("Supplier: ")
        supplierLayout.addWidget(supplierLabel)
        self.supplier = QComboBox()
        self.supplier.addItem("Select a Supplier...") #placeholder text
        self.supplier.setCurrentIndex(0)
        self.supplier.model().item(0).setEnabled(False) #make the placeholder unselectable
        self.supplier.addItem("All")
        self.updateSuppliers()
        supplierLayout.addWidget(self.supplier)
        supplierContainer.setLayout(supplierLayout)
        self.layout.addWidget(supplierContainer, alignment=Qt.AlignLeft)

        # Categories
        categoryLabel = QLabel("Categories: ")
        self.layout.addWidget(categoryLabel)
        categoryList = [
            "Groceries",
            "Beverages",
            "Household",
            "Personal Care",
            "Baby and Childcare",
            "Pet Supplies",
            "Hardware and Tools",
            "Electronics",
            "Clothing",
            "General",
            "Stationary"
        ]
        self.categories = CheckBoxListWidget(categoryList)
        self.layout.addWidget(self.categories)



        self.setLayout(self.layout)

    def updateStores(self):
        conn = connect()
        cursor = conn.cursor()

        sql = f"SELECT store_num, store_name, city, state FROM location"
        cursor.execute(sql)
        stores = cursor.fetchall()
        for store_num, store_name, city, state in stores:
            self.storeSelect.addItem(f"#{store_num} - {store_name}, {city}, {state}", store_num)
        self.layout.addWidget(self.storeSelect)
        conn.close()

    def updateSuppliers(self):
        conn = connect()
        cursor = conn.cursor()

        sql = f"SELECT supplier_id, supplier_name FROM supplier"
        cursor.execute(sql)
        suppliers = cursor.fetchall()
        for supplier_id, supplier_name in suppliers:
            self.supplier.addItem(f"{supplier_name} - {supplier_id}", supplier_id)
        conn.close()