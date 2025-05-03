from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox,
    QPushButton, QListWidget, QLabel
)
from db import connect

class SupplierSearchWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        # Top search bar layout
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search term...")

        self.filter_dropdown = QComboBox()
        self.filter_dropdown.addItems(["supplier_name", "city", "state", "supplier_id"])

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.perform_search)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.filter_dropdown)
        search_layout.addWidget(self.search_button)

        # Results list
        self.results_list = QListWidget()
        self.results_list.itemClicked.connect(self.on_item_clicked)
        self.results_data = []  # tuples of form ("string", supplier_id)

        self.layout.addLayout(search_layout)
        self.layout.addWidget(QLabel("Matching Suppliers:"))
        self.layout.addWidget(self.results_list)

        # Text box that shows the currently selected supplier
        self.selected_supplier = QLineEdit()
        self.selected_supplier.setPlaceholderText("Select a Supplier")
        self.selected_supplier.setReadOnly(True)
        self.layout.addWidget(self.selected_supplier)

        self.setLayout(self.layout)

        #by default have search loaded in
        self.perform_search()

    def perform_search(self):
        query = self.search_input.text()
        filter_by = self.filter_dropdown.currentText()

        conn = connect()
        cursor = conn.cursor()

        if filter_by == "supplier_id":
            if not query.isdigit():
                self.results_list.clear()
                return
            sql = "SELECT supplier_id, supplier_name, city, state FROM supplier WHERE supplier_id = %s"
            cursor.execute(sql, (int(query),))
        else:
            sql = f"SELECT supplier_id, supplier_name, city, state FROM supplier WHERE {filter_by} ILIKE %s"
            cursor.execute(sql, (f"%{query}%",))

        results = cursor.fetchall()

        self.results_list.clear()
        self.results_data.clear()

        for supplier_id, name, city, state in results:
            self.results_list.addItem(f"#{supplier_id} - {name}, {city}, {state}")
            self.results_data.append((f"#{supplier_id} - {name}, {city}, {state}", supplier_id))

        cursor.close()
        conn.close()


    def get_selected_supplier_id(self):
        if self.results_list.currentItem() == "":
            return ""
        return self.results_data[self.results_list.currentRow()][1]

    def on_item_clicked(self):
        selected_supplier = self.results_list.currentItem()
        self.selected_supplier.setText(selected_supplier.text())
