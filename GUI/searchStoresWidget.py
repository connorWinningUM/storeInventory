from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox,
    QPushButton, QListWidget, QLabel
)
from db import connect

class StoreSearchWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        # Top search bar layout
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search term...")

        self.filter_dropdown = QComboBox()
        self.filter_dropdown.addItems(["store_name", "city", "state"])

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.perform_search)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.filter_dropdown)
        search_layout.addWidget(self.search_button)

        # Results list
        self.results_list = QListWidget()
        self.results_list.itemClicked.connect(self.on_item_clicked)
        self.results_data = [] # add tuples of form ("string", store_num), should have same indexes as results_list

        self.layout.addLayout(search_layout)
        self.layout.addWidget(QLabel("Matching Stores:"))
        self.layout.addWidget(self.results_list)

        # A text box that shows the current selected store
        self.selected_store = QLineEdit()
        self.selected_store.setPlaceholderText("Select a Store")
        self.selected_store.setReadOnly(True)
        self.layout.addWidget(self.selected_store)

        self.setLayout(self.layout)

    def perform_search(self):
        query = self.search_input.text()
        filter_by = self.filter_dropdown.currentText()

        conn = connect()
        cursor = conn.cursor()

        sql = f"SELECT store_num, store_name, city, state FROM location WHERE {filter_by} ILIKE %s"
        cursor.execute(sql, (f"%{query}%",))
        results = cursor.fetchall()

        self.results_list.clear()
        for store_num, store_name, city, state in results:
            self.results_list.addItem(f"#{store_num} - {store_name}, {city}, {state}")
            self.results_data.append((f"#{store_num} - {store_name}, {city}, {state}", store_num))

        cursor.close()
        conn.close()

    def get_selected_store_num(self):
        return self.results_data[self.results_list.currentRow()][1]

    def on_item_clicked(self):
        selected_store = self.results_list.currentItem()
        self.selected_store.setText(selected_store.text())