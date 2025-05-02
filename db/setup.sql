DROP TABLE IF EXISTS backorder, supplies, item, employee, supplier, location CASCADE;

CREATE TABLE location (
    store_num INT PRIMARY KEY,
    store_name VARCHAR(45) NOT NULL,
    street_address VARCHAR(45) NOT NULL,
    city VARCHAR(45) NOT NULL,
    state VARCHAR(45) NOT NULL,
    zip_code INT NOT NULL
);

CREATE TABLE supplier(
    supplier_id INTEGER PRIMARY KEY,
    supplier_name VARCHAR(100),
    street_address VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code INTEGER NOT NULL
);

CREATE TABLE employee (
    ssn CHAR(9) PRIMARY KEY,              
    name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL, 
    password VARCHAR(255) NOT NULL,       
    role VARCHAR(50) NOT NULL DEFAULT 'employee',            
    store_num INTEGER NOT NULL, 
    FOREIGN KEY (store_num) REFERENCES location(store_num)    
);

CREATE TABLE item (
    barcode INT PRIMARY KEY,
    name VARCHAR(25) NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    description VARCHAR(250),
    category VARCHAR(50) DEFAULT 'general',
    cost DECIMAL(10, 2) NOT NULL,
    store_num INT NOT NULL,
    FOREIGN KEY (store_num) REFERENCES location(store_num)
);

CREATE TABLE IF NOT EXISTS supplies (
    supplier_id INT NOT NULL,
    barcode INT NOT NULL,
    PRIMARY KEY (supplier_id, barcode),
    FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id),
    FOREIGN KEY (barcode) REFERENCES item(barcode)
);

CREATE TABLE backorder(
    order_num INTEGER PRIMARY KEY,
    complete_date DATE DEFAULT '2000-01-01',
    start_date DATE NOT NULL,
    quantity INTEGER NOT NULL DEFAULT -1,
    employee_ssn CHAR(9) NOT NULL,
    barcode INT NOT NULL,
    supplier_id INT NOT NULL,
    store_num INT NOT NULL,
    FOREIGN KEY (employee_ssn) REFERENCES employee(ssn),
    FOREIGN KEY (barcode) REFERENCES item(barcode),
    FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id),
    FOREIGN KEY (store_num) REFERENCES location(store_num)
);

-- insert default testing data --
INSERT INTO location (store_num, store_name, street_address, city, state, zip_code) VALUES
(1, 'Main Street Store', '123 Main St', 'Springfield', 'IL', 62704),
(2, 'Downtown Outlet', '456 Elm St', 'Chicago', 'IL', 60616),
(20, 'Lakeside Branch', '789 Shore Dr', 'Evanston', 'IL', 60201);

INSERT INTO supplier (supplier_id, supplier_name, street_address, city, state, zip_code) VALUES
(101, 'Acme Supplies', '789 Oak St', 'Peoria', 'IL', 61614),
(102, 'Global Goods', '321 Pine St', 'Naperville', 'IL', 60540);

INSERT INTO employee (ssn, name, username, password, role, store_num) VALUES
('123456789', 'Alice Smith', 'asmith', 'password123', 'manager', 1),
('987654321', 'Bob Johnson', 'bjohnson', 'securepass', 'employee', 2);

INSERT INTO item (barcode, name, quantity, description, category, cost, store_num) VALUES
(1001, 'Toothpaste', 50, 'Sensodyne Sensitivity & Gum Mint toothpaste is a dual action toothpaste thats specifically designed to help people with both sensitivity and early gum problems.', 
    'Personal Care', 1.99, 1),
(2002, 'Shampoo', 30, 'HARD WORKING, LONG LASTING Your haircare should work as hard as you do. Pantene Pro-V Daily Moisture Renewal Shampoo cleanses parched hair with a potent blend of nutrients to remove buildup and prime your strands for optimal hydration. ',
    'Personal Care', 3.99, 1),
(2003, 'Notebook', 100, ' Inside Pockets is an essential tool for school, work, or home. This one-subject notebook features 100 college-ruled sheets of heavyweight paper and inside pockets to help you organize handouts.',
    'Stationery', 2.49, 1),
(2004, '4K 55in TV', 20, 'Upgrade your home theater with this stylish 4K TV featuring vibrant colors, rich contrast and an advanced 4K processor.',
    'Electronics', 378.00, 20),
(2001, 'Wireless Earbuds', 45, 'Experience immersive sound with these comfortable wireless earbuds. Features include active noise cancellation, water resistance, and 8-hour battery life with additional 24 hours from the charging case.',
    'Electronics', 89.99, 2),
(1002, 'Dental Floss', 75, 'Mint-flavored waxed dental floss that easily glides between teeth to remove plaque and food particles. Recommended by dentists for daily oral hygiene to help prevent cavities and gum disease.',
    'Personal Care', 1.49, 1);


INSERT INTO supplies (supplier_id, barcode) VALUES 
(101, 2001),
(101, 2002),
(102, 2003),
(102, 2004);

INSERT INTO backorder (order_num, complete_date, start_date, quantity, employee_ssn, barcode, supplier_id, store_num) VALUES
(1, '2024-10-10', '2024-09-30', 10, '123456789', 1001, 101, 1),
(2, NULL, '2024-10-05', 5, '987654321', 1002, 102, 2);

INSERT INTO employee (ssn, name, username, password, role, store_num) VALUES
(123123123, 'ADMIN', 'admin', 'password', 'admin', 1);


-- this view is used to query the items because it will include the supplier_id and name --
CREATE OR REPLACE VIEW item_suppliers AS
    SELECT
        i.barcode,
        i.name AS item_name,
        i.category,
        i.description,
        i.cost,
        i.quantity,
        sup.supplier_name,
        s.supplier_id,
        i.store_num
    FROM 
        item i
    JOIN 
        supplies s ON i.barcode = s.barcode
    JOIN
        supplier sup ON s.supplier_id = sup.supplier_id;