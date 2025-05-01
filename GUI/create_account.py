from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QLabel, QComboBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from db import connect
from GUI.searchStoresWidget import StoreSearchWidget

class CreateAccount(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.layout = QFormLayout()

        main_layout = QHBoxLayout()
        left_container = QWidget()

        self.stacked_widget = stacked_widget

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.reinput_password_input = QLineEdit()
        self.reinput_password_input.setEchoMode(QLineEdit.Password)

        self.layout.addRow("Username:", self.username_input)
        self.layout.addRow("Password:", self.password_input)
        self.layout.addRow("Reinput Password:", self.reinput_password_input)

        self.ssn_input = QLineEdit()
        self.ssn_input.setValidator(QIntValidator())
        self.ssn_input.setMaxLength(9)
        self.layout.addRow("SSN: ", self.ssn_input)

        self.name_input = QLineEdit()
        self.layout.addRow("Name: ", self.name_input)

        self.role_input = QComboBox()
        self.role_input.addItems(["Employee", "Manager", "Admin"])
        self.layout.addRow("Role: ", self.role_input)

        #put all of the previously added rows to the left container
        left_container.setLayout(self.layout)

        right_container = QWidget()
        right_layout = QVBoxLayout()
        
        search_label = QLabel("Search Store:")
        self.search_stores = StoreSearchWidget()
        
        right_layout.addWidget(search_label)
        right_layout.addWidget(self.search_stores)
        right_layout.addStretch(1)  # Push everything to the top
        
        right_container.setLayout(right_layout)

        #done with the right hand side
        spacer_label = QLabel()
        self.layout.addRow("", spacer_label)

        accept_button = QPushButton("Create Account")
        accept_button.clicked.connect(self.on_accept_button_pressed)
        self.layout.addWidget(accept_button)

        self.error_label = QLabel(self)
        self.error_label.setStyleSheet("color: red; font-weight: bold;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setText("")  # No error by default
        self.layout.addWidget(self.error_label)

        main_layout.addWidget(left_container)  # Allocate more space to the form
        main_layout.addWidget(right_container)  # Allocate less space to the search

        self.setLayout(main_layout)

    def on_accept_button_pressed(self):
        username = self.username_input.text()
        password = self.password_input.text()
        re_password = self.reinput_password_input.text()
        ssn = self.ssn_input.text()
        name = self.name_input.text()
        role = self.role_input.currentText()
        store_num = self.search_stores.get_selected_store_num()

        # Check for empty username
        if not username:
            self.error_label.setText("Please enter a username.")
            return

        # Check for empty password
        if not password:
            self.error_label.setText("Please enter a password.")
            return

        # Check if passwords match
        if password != re_password:
            self.error_label.setText("Passwords do not match.")
            return

        # Connect to the database
        conn = connect()
        cursor = conn.cursor()

        # Check if username already exists
        cursor.execute("SELECT * FROM employee WHERE username = %s", (username,))
        if cursor.fetchone():
            self.error_label.setText("Username is taken, choose a different username.")
            cursor.close()
            conn.close()
            return

        # Add user to the database
        cursor.execute(
        "INSERT INTO employee (ssn, name, username, password, role, store_num) VALUES (%s, %s, %s, %s, %s, %s)",
        (ssn, name, username, password, role, store_num)
        )
        conn.commit()
        cursor.close()
        conn.close()

        self.stacked_widget.setCurrentIndex(0)