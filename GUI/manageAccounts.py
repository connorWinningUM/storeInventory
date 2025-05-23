from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QLabel
from PyQt5.QtCore import Qt
from db import connect

class ManageAccounts(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.layout = QHBoxLayout()
        self.stacked_widget = stacked_widget

        # Layout for the buttons on the left side
        buttonsContainer = QWidget()
        buttonsLayout = QVBoxLayout()

        # Back
        go_back = QPushButton("Back")
        go_back.clicked.connect(self.on_back_pressed)
        buttonsLayout.addWidget(go_back)

        # Delete Account
        delete = QPushButton("Delete Account")
        delete.clicked.connect(self.on_delete_pressed)
        buttonsLayout.addWidget(delete)

        # Edit Account
        edit = QPushButton("Edit Account")
        edit.clicked.connect(self.on_edit_pressed)
        #buttonsLayout.addWidget(edit)

        # Add a spacer to push create account to bottom
        buttonsLayout.addStretch()

        # Account Stats
        stats = QPushButton("Account Statistics")
        stats.clicked.connect(self.on_stats_pressed)
        buttonsLayout.addWidget(stats)

        # Create Account
        create_account = QPushButton("Create Account")
        create_account.clicked.connect(self.on_create_account)
        buttonsLayout.addWidget(create_account)


        # Put into container and layout
        buttonsContainer.setLayout(buttonsLayout)
        self.layout.addWidget(buttonsContainer, 1)

        # Container for the account list
        accountsContainer = QWidget()
        accountsLayout = QVBoxLayout()

        # List for the accounts
        self.accountList = QTableWidget()
        headers = [
            "Username",
            "Role",
            "Name",
            "Store Num"
        ]
        self.accountList.setColumnCount(len(headers))
        self.accountList.setHorizontalHeaderLabels(headers)
        self.update_account_list()
        self.accountList.itemClicked.connect(self.on_account_clicked)
        accountsLayout.addWidget(self.accountList)

        # Selected Account
        self.selectedAccount = QLineEdit()
        self.selectedAccount.setPlaceholderText("Select An Account")
        self.selectedAccount.setReadOnly(True)
        accountsLayout.addWidget(self.selectedAccount)

        # Error Label
        self.errorLabel = QLabel()
        self.errorLabel.setStyleSheet("color: red; font-weight: bold;")
        self.errorLabel.setAlignment(Qt.AlignCenter)
        self.errorLabel.setText("")

        # Add the Account container to the layout
        accountsContainer.setLayout(accountsLayout)
        self.layout.addWidget(accountsContainer, 5)


        self.setLayout(self.layout)

    def on_delete_pressed(self):
        # Get essn of currently selected account
        accountUsername = self.selectedAccount.text()
        print(accountUsername)
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT ssn, role FROM employee WHERE username = %s", (accountUsername,))
        account = cursor.fetchone()
        if account[1] == "admin":
            self.errorLabel.setText("Cannot Delete Admin Account")
            return
        
        # get admin ssn for the next step
        cursor.execute("SELECT ssn FROM employee WHERE username = %s", ('admin',))
        adminSSN = cursor.fetchone()

        # before deleting the employee, must change ssn on backorders to the admin account
        cursor.execute("""
            UPDATE backorder 
            SET employee_ssn = %s 
            WHERE employee_ssn = %s
        """, (adminSSN, account[0]))

        # now delete the employee from the database
        cursor.execute("DELETE FROM employee WHERE ssn = %s", (account[0],))

        conn.commit()
        cursor.close()
        conn.close()

        self.update_account_list()
    
    def on_edit_pressed(self):
        accountUsername = self.selectedAccount.text()
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT ssn FROM employee WHERE username = %s", (accountUsername,))
        account = cursor.fetchone()

    
    def on_back_pressed(self):
        self.stacked_widget.setCurrentIndex(1)

    def on_create_account(self):
        self.stacked_widget.setCurrentIndex(4)

    def on_stats_pressed(self):
        self.stacked_widget.widget(5).update_back_index(3)
        self.stacked_widget.widget(5).update_statistics()
        self.stacked_widget.setCurrentIndex(5)

    def get_accounts(self):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT username, role, name, store_num FROM employee")
        accounts = cursor.fetchall()
        cursor.close()
        conn.close()
        return accounts
    
    def update_account_list(self):
        self.accounts = self.get_accounts()

        self.accountList.setRowCount(len(self.accounts))

        for row_idx, row_data in enumerate(self.accounts):
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    self.accountList.setItem(row_idx, col_idx, item)

    def on_account_clicked(self):
        itemIndex = self.accountList.currentRow()
        account = self.accounts[itemIndex]
        self.selectedAccount.setText(account[0])
        