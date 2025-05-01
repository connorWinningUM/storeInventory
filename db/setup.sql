DROP TABLE IF EXISTS backorder, item, employee, supplier, location CASCADE;

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
    description VARCHAR(45),
    cost DECIMAL(10, 2) NOT NULL,
    store_num INT NOT NULL,
    FOREIGN KEY (store_num) REFERENCES location(store_num)
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