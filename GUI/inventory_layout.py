from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QPushButton, QVBoxLayout, QFormLayout, QTableWidget, QLabel, QTableWidgetItem
from GUI.inventoryTaskbar import inventoryTaskbar
from db import connect

class InventoryLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()

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
        self.layout.addWidget(self.queryLabel)

        self.rightSideLayout = QVBoxLayout()
        rightContainer = QWidget()
        # Inventory list
        self.inventoryList = QTableWidget()
        headers = ["Barcode", "Name", "Category", "Item Description", "Cost", "Quantity", "Supplier Name", "Supplier ID", "Store Number"]
        self.inventoryList.setColumnCount(len(headers))
        self.inventoryList.setHorizontalHeaderLabels(headers)
        self.rightSideLayout.addWidget(self.inventoryList)

        # Refresh button
        refresh_btn = QPushButton("Refresh Inventory")
        self.rightSideLayout.addWidget(refresh_btn)

        # Add Item button
        add_item_btn = QPushButton("Go to Add Item")
        self.rightSideLayout.addWidget(add_item_btn)

        rightContainer.setLayout(self.rightSideLayout)
        self.layout.addWidget(rightContainer, stretch=3)
        self.setLayout(self.layout)

    def on_search(self):
        store_num = self.taskBar.storeSelect.currentData()
        searchBy = self.taskBar.searchBy.currentData()
        searchTerm = self.taskBar.search_bar_input.text()
        sortBy = self.taskBar.sortByList.currentData()
        quantityMin = self.taskBar.quantityMin.text()
        quantityMax = self.taskBar.quantityMax.text()
        print(quantityMin)
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

            print(results)

            for row_idx, row_data in enumerate(results):
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    self.inventoryList.setItem(row_idx, col_idx, item)

            self.queryLabel.setText(f"Found {len(results)} matching items")

        except Exception as e:
            self.queryLabel.setText(f"Error executing query: {e}")
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
            query += f" ORDER BY {sortBy}"

        return query, params



