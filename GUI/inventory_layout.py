from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QPushButton, QVBoxLayout, QFormLayout, QTableWidget, QLabel, QTableWidgetItem
from GUI.inventoryTaskbar import inventoryTaskbar
from db import connect

class InventoryLayout(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.layout = QHBoxLayout()
        self.stacked_widget = stacked_widget
        
        # Inventory TaskBar
        self.taskBar = inventoryTaskbar(self.on_search)
        leftContainer = QWidget()
        taskLayout = QFormLayout()
        taskLayout.addWidget(self.taskBar)
        leftContainer.setLayout(taskLayout)
        self.layout.addWidget(leftContainer, stretch=1)

        # add query label
        self.queryLabel = QLabel(self)
        self.queryLabel.setText("")

        self.rightSideLayout = QVBoxLayout()
        rightContainer = QWidget()
        # Inventory list
        self.inventoryList = QTableWidget()
        headers = ["Barcode", "Name", "Category", "Item Description", "Cost", "Quantity", "Supplier Name", "Supplier ID", "Store Number", "Backorder Count"]
        self.inventoryList.setColumnCount(len(headers))
        self.inventoryList.setHorizontalHeaderLabels(headers)
        self.rightSideLayout.addWidget(self.queryLabel)
        self.rightSideLayout.addWidget(self.inventoryList)

        # MenuBar
        inventoryActionsContainer = QWidget()
        self.inventoryActionsLayout = QHBoxLayout()
        self.usernameLabel = QLabel()
        logoutBtn = QPushButton("Logout")
        logoutBtn.clicked.connect(self.on_logout_pressed)
        self.manageAccounts = QPushButton("Manage Accounts")
        self.manageAccounts.clicked.connect(self.on_manage_accounts_pressed)
        self.statistics = QPushButton("View Statistics")
        self.statistics.clicked.connect(self.on_statistics_pressed)
        add_item_btn = QPushButton("+ Add Item")
        add_item_btn.clicked.connect(self.on_add_item_pressed)
        make_backorder_button = QPushButton("Create Backorder")
        self.inventoryActionsLayout.addWidget(self.usernameLabel)
        self.inventoryActionsLayout.addWidget(logoutBtn)
        #self.inventoryActionsLayout.addWidget(self.manageAccounts)
        self.inventoryActionsLayout.addWidget(add_item_btn)
        self.inventoryActionsLayout.addWidget(make_backorder_button)
        inventoryActionsContainer.setLayout(self.inventoryActionsLayout)
        self.layout.setMenuBar(inventoryActionsContainer)

        rightContainer.setLayout(self.rightSideLayout)
        self.layout.addWidget(rightContainer, stretch=3)
        self.setLayout(self.layout)

        #have items loaded in by default
        self.on_search()

    def on_search(self):
        store_num = self.taskBar.storeSelect.currentData()
        searchBy = self.taskBar.searchBy.currentData()
        searchTerm = self.taskBar.search_bar_input.text()
        sortBy = self.taskBar.sortByList.currentData()
        quantityMin = self.taskBar.quantityMin.text()
        quantityMax = self.taskBar.quantityMax.text()
        supplier = self.taskBar.supplier.currentData()
        ignoreSupplier = False
        categories = self.taskBar.categories.get_checked_items()
        ignoreCategories = False

        # check for no inputs, set default values
        if searchTerm == "":
            searchTerm = '*'
        if quantityMax == "":
            quantityMax = 9999999
        else:
            quantityMax = int(quantityMax)
        if quantityMin == "":
            quantityMin = 0
        else:
            quantityMin = int(quantityMin)
        if supplier is None:
            ignoreSupplier = True
        if not categories:
            ignoreCategories = True

        # build the query
        query, params = self.buildSearchQuery(store_num, searchBy, searchTerm, sortBy, quantityMin, quantityMax, 
               supplier, ignoreSupplier, categories, ignoreCategories)

        # execute the query
        conn = connect()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
            self.inventoryList.setRowCount(0)

            #if there are no results
            if not results:
                self.queryLabel.setText("No Results Found.")
                return
            
            #populate the table
            self.inventoryList.setRowCount(len(results))

            for row_idx, row_data in enumerate(results):
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    self.inventoryList.setItem(row_idx, col_idx, item)

            self.queryLabel.setText(f"Found {len(results)} matching items")

        except Exception as e:
            print(e)
        finally:
            conn.close()
    
    def buildSearchQuery(self, store_num, searchBy, searchTerm, sortBy, quantityMin, quantityMax, 
               supplier, ignoreSupplier, categories, ignoreCategories):
        query = f"SELECT * FROM item_suppliers WHERE store_num = {store_num}"
        params = [] # prevents SQL injection attacks, will replace %s symbols when executed by cursor

        # search term
        if searchTerm != "*":
            if searchBy == "barcode":
                query += f" AND {searchBy}::text LIKE %s"
                params.append(f"%{searchTerm}%")
            else:
                query += f" AND {searchBy} LIKE %s"
                params.append(f"%{searchTerm}%")
        
        # quantity
        query += " AND quantity >= %s AND quantity <= %s"
        params.append(quantityMin)
        params.append(quantityMax)

        # supplier
        if not ignoreSupplier:
            query += " AND supplier_id = %s"
            params.append(supplier)

        # categories
        if not ignoreCategories and categories:
            placeholders = ", ".join(["%s" for _ in categories])
            query += f" AND category IN ({placeholders})"
            params.extend(categories)

        # sort by
        if sortBy:
            if sortBy == "backorder_count":
                print("BACK ORDER QUERY")
            else:
                query += f" ORDER BY {sortBy}"

        return query, params

    def on_add_item_pressed(self):
        self.stacked_widget.widget(2).pass_username(self.username)
        self.stacked_widget.setCurrentIndex(2)

    def passUsername(self, username):
        self.username = username
        self.usernameLabel.setText(f"[{self.username}]")
    
    def passRole(self, role):
        self.role = role
        if role == "admin" or role == "manager":
            self.inventoryActionsLayout.addWidget(self.manageAccounts)
            self.inventoryActionsLayout.addWidget(self.statistics)

    def on_logout_pressed(self):
        self.username = ""
        self.stacked_widget.setCurrentIndex(0)

    def on_manage_accounts_pressed(self):
        return
    
    def on_statistics_pressed(self):
        self.stacked_widget.setCurrentIndex(5)


