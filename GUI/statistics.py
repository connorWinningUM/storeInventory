from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel, QGridLayout
from db import connect
from PyQt5.QtCore import Qt
from GUI.checkBoxList import CheckBoxListWidget
from PyQt5.QtGui import QIntValidator

class InventoryStatistics(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.connection = connect()
        self.initUI()
        
    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Inventory Statistics")
        title.setStyleSheet("font-size: 18pt; font-weight: bold;")
        main_layout.addWidget(title)
        
        # Create tabs for each stat
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # Create tabs
        backorder_tab = self.createBackorderTab()
        tabs.addTab(backorder_tab, "Backorder Statistics")
        
        store_tab = self.createStoreTab()
        tabs.addTab(store_tab, "Store Statistics")
        
        item_tab = self.createItemTab()
        tabs.addTab(item_tab, "Inventory Statistics")
        
        employee_tab = self.createEmployeeTab()
        tabs.addTab(employee_tab, "Employee Stats")

        self.connection.close()
        
    def createBackorderTab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Main container
        stats_grid = QGridLayout()
        layout.addLayout(stats_grid)
        
        cursor = self.connection.cursor()
        row = 0          # keeps track of which row to add
        
        # Total backorders count
        cursor.execute("SELECT COUNT(*) FROM backorder")
        total_orders = cursor.fetchone()[0]
        stats_grid.addWidget(QLabel("Total Backorders:"), row, 0)
        stats_grid.addWidget(QLabel(str(total_orders)), row, 1)
        row += 1
        
        # Average backorder quantity
        cursor.execute("SELECT AVG(quantity) FROM backorder")
        average_quantity = cursor.fetchone()[0]
        stats_grid.addWidget(QLabel("Average Backorder Quantity:"), row, 0)
        stats_grid.addWidget(QLabel(f"{average_quantity:.2f}"), row, 1)
        row += 1
        
        # Total items on backorder
        cursor.execute("SELECT SUM(quantity) FROM backorder")
        total_items = cursor.fetchone()[0]
        stats_grid.addWidget(QLabel("Total Items on Backorder:"), row, 0)
        stats_grid.addWidget(QLabel(str(total_items)), row, 1)
        row += 1
        
        # Backorders by each employee
        cursor.execute("""
            SELECT e.name, COUNT(*) as orders_count
            FROM backorder b
            JOIN employee e ON b.employee_ssn = e.ssn
            GROUP BY e.name
            ORDER BY orders_count DESC
        """)
        
        employee_orders = cursor.fetchall()
        stats_grid.addWidget(QLabel("Backorders by Employee:"), row, 0, 1, 2)
        row += 1
        
        for name, count in employee_orders:
            stats_grid.addWidget(QLabel(f"  • {name}:"), row, 0)
            stats_grid.addWidget(QLabel(str(count)), row, 1)
            row += 1
        
        # Average time for backorder completion
        cursor.execute("""
            SELECT AVG(complete_date - start_date) as avg_days
            FROM backorder
            WHERE complete_date IS NOT NULL AND complete_date != '2000-01-01'
        """)
        avg_days = cursor.fetchone()[0]
        if avg_days:
            stats_grid.addWidget(QLabel("Average Days to Complete Backorder:"), row, 0)
            stats_grid.addWidget(QLabel(f"{avg_days:.1f} days"), row, 1)
        
        return tab
    
    def createStoreTab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        stats_grid = QGridLayout()
        layout.addLayout(stats_grid)
        
        cursor = self.connection.cursor()
        row = 0
        
        # Item count by store
        cursor.execute("""
            SELECT l.store_name, COUNT(*) as item_count
            FROM item i
            JOIN location l ON i.store_num = l.store_num
            GROUP BY l.store_name
            ORDER BY item_count DESC
        """)
        
        store_items = cursor.fetchall()
        stats_grid.addWidget(QLabel("Items by Store:"), row, 0, 1, 2)
        row += 1
        
        for store, count in store_items:
            stats_grid.addWidget(QLabel(f"  • {store}:"), row, 0)
            stats_grid.addWidget(QLabel(str(count)), row, 1)
            row += 1
        
        # Employee count by store
        cursor.execute("""
            SELECT l.store_name, COUNT(*) as employee_count
            FROM employee e
            JOIN location l ON e.store_num = l.store_num
            GROUP BY l.store_name
            ORDER BY employee_count DESC
        """)
        
        store_employees = cursor.fetchall()
        stats_grid.addWidget(QLabel("Employees by Store:"), row, 0, 1, 2)
        row += 1
        
        for store, count in store_employees:
            stats_grid.addWidget(QLabel(f"  • {store}:"), row, 0)
            stats_grid.addWidget(QLabel(str(count)), row, 1)
            row += 1
        
        # Total inventory value by store
        cursor.execute("""
            SELECT l.store_name, SUM(i.cost * i.quantity) as total_value
            FROM item i
            JOIN location l ON i.store_num = l.store_num
            GROUP BY l.store_name
            ORDER BY total_value DESC
        """)
        
        store_values = cursor.fetchall()
        stats_grid.addWidget(QLabel("Total Inventory Value by Store:"), row, 0, 1, 2)
        row += 1
        
        for store, value in store_values:
            stats_grid.addWidget(QLabel(f"  • {store}:"), row, 0)
            stats_grid.addWidget(QLabel(f"${value:.2f}"), row, 1)
            row += 1
        
        return tab
    
    def createItemTab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        stats_grid = QGridLayout()
        layout.addLayout(stats_grid)
        
        cursor = self.connection.cursor()
        row = 0
        
        # Total items
        cursor.execute("SELECT COUNT(*) FROM item")
        total_items = cursor.fetchone()[0]
        stats_grid.addWidget(QLabel("Total Item Types:"), row, 0)
        stats_grid.addWidget(QLabel(str(total_items)), row, 1)
        row += 1
        
        # Total quantity
        cursor.execute("SELECT SUM(quantity) FROM item")
        total_quantity = cursor.fetchone()[0]
        stats_grid.addWidget(QLabel("Total Items in Inventory:"), row, 0)
        stats_grid.addWidget(QLabel(str(total_quantity)), row, 1)
        row += 1
        
        # Average cost
        cursor.execute("SELECT AVG(cost) FROM item")
        avg_cost = cursor.fetchone()[0]
        stats_grid.addWidget(QLabel("Average Item Cost:"), row, 0)
        stats_grid.addWidget(QLabel(f"${avg_cost:.2f}"), row, 1)
        row += 1
        
        # Highest cost item
        cursor.execute("SELECT name, cost FROM item ORDER BY cost DESC LIMIT 1")
        highest_item = cursor.fetchone()
        stats_grid.addWidget(QLabel("Most Expensive Item:"), row, 0)
        stats_grid.addWidget(QLabel(f"{highest_item[0]} (${highest_item[1]:.2f})"), row, 1)
        row += 1
        
        # Items by category
        cursor.execute("""
            SELECT category, COUNT(*) as count, SUM(quantity) as total_quantity
            FROM item
            GROUP BY category
            ORDER BY count DESC
        """)
        
        categories = cursor.fetchall()
        stats_grid.addWidget(QLabel("Items by Category:"), row, 0, 1, 2)
        row += 1
        
        for category, count, quantity in categories:
            stats_grid.addWidget(QLabel(f"  • {category}:"), row, 0)
            stats_grid.addWidget(QLabel(f"{count} types ({quantity} total items)"), row, 1)
            row += 1
        
        # Total inventory value
        cursor.execute("SELECT SUM(cost * quantity) FROM item")
        total_value = cursor.fetchone()[0]
        stats_grid.addWidget(QLabel("Total Inventory Value:"), row, 0)
        stats_grid.addWidget(QLabel(f"${total_value:.2f}"), row, 1)
        
        return tab
    
    def createEmployeeTab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        stats_grid = QGridLayout()
        layout.addLayout(stats_grid)
        
        cursor = self.connection.cursor()
        row = 0
        
        # Total employees
        cursor.execute("SELECT COUNT(*) FROM employee")
        total_employees = cursor.fetchone()[0]
        stats_grid.addWidget(QLabel("Total Employees:"), row, 0)
        stats_grid.addWidget(QLabel(str(total_employees)), row, 1)
        row += 1
        
        # Employees by role
        cursor.execute("""
            SELECT role, COUNT(*) as count
            FROM employee
            GROUP BY role
            ORDER BY count DESC
        """)
        
        roles = cursor.fetchall()
        stats_grid.addWidget(QLabel("Employees by Role:"), row, 0, 1, 2)
        row += 1
        
        for role, count in roles:
            stats_grid.addWidget(QLabel(f"  • {role}:"), row, 0)
            stats_grid.addWidget(QLabel(str(count)), row, 1)
            row += 1
        
        # Backorders per employee
        cursor.execute("""
            SELECT e.name, COUNT(b.order_num) as order_count
            FROM employee e
            LEFT JOIN backorder b ON e.ssn = b.employee_ssn
            GROUP BY e.name
            ORDER BY order_count DESC
        """)
        
        employee_orders = cursor.fetchall()
        stats_grid.addWidget(QLabel("Backorders Handled by Employee:"), row, 0, 1, 2)
        row += 1
        
        for name, count in employee_orders:
            stats_grid.addWidget(QLabel(f"  • {name}:"), row, 0)
            stats_grid.addWidget(QLabel(str(count)), row, 1)
            row += 1
        
        return tab