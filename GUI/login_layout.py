from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from db import connect

class LoginLayout(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.layout = QFormLayout()

        self.stacked_widget = stacked_widget

        # Login fields
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.layout.addRow("Username:", self.username_input)
        self.layout.addRow("Password:", self.password_input)

        # Login button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.on_login_pressed)
        self.layout.addWidget(login_btn)

        # create account button
        create_account_btn = QPushButton("Create Account")
        create_account_btn.clicked.connect(self.on_create_account_pressed)
        self.layout.addWidget(create_account_btn)

        # Error Label
        self.error_label = QLabel(self)
        self.error_label.setStyleSheet("color: red; font-weight: bold;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setText("")  # No error by default
        self.layout.addWidget(self.error_label)

        # Create a container to center and set width
        contentContainer = QWidget()
        contentContainer.setLayout(self.layout)
        contentContainer.setFixedWidth(400)
        mainLayout = QHBoxLayout()
        mainLayout.addStretch(1)   #adds a strech on the left
        mainLayout.addWidget(contentContainer, alignment=Qt.AlignCenter)
        mainLayout.addStretch(1)   #adds a strech on the right


        self.setLayout(mainLayout)

    def on_login_pressed(self):
        username = self.username_input.text()
        password_input = self.password_input.text()
        

        #query for username and password
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM employee WHERE username = %s", (username,))
        passwords = cursor.fetchall()
        cursor.close()
        conn.close()

        if(len(passwords) > 1):
            self.error_label.setText("Database Error: More Than 1 Account with username: " + username)
            return
        if(len(passwords) == 0):
            self.error_label.setText("Incorrect Login Credentials: Username Unknown")
            return

        if(passwords[0][0] == password_input):
            self.username_input.clear()
            self.password_input.clear()
            self.stacked_widget.widget(1).passUsername(username)
            self.stacked_widget.setCurrentIndex(1)
        else:
            self.error_label.setText("Incorrect Login Credentials: Incorrect Password")

    def on_create_account_pressed(self):
        self.stacked_widget.setCurrentIndex(4)
