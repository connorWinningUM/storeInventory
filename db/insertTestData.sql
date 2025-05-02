INSERT INTO location (store_num, store_name, street_address, city, state, zip_code) VALUES
(1, 'Main Street Store', '123 Main St', 'Springfield', 'IL', 62704),
(2, 'Downtown Outlet', '456 Elm St', 'Chicago', 'IL', 60616);

INSERT INTO supplier (supplier_id, supplier_name, street_address, city, state, zip_code) VALUES
(101, 'Acme Supplies', '789 Oak St', 'Peoria', 'IL', 61614),
(102, 'Global Goods', '321 Pine St', 'Naperville', 'IL', 60540);

INSERT INTO employee (ssn, name, username, password, role, store_num) VALUES
('123456789', 'Alice Smith', 'asmith', 'password123', 'manager', 1),
('987654321', 'Bob Johnson', 'bjohnson', 'securepass', 'employee', 2);

INSERT INTO item (barcode, name, quantity, description, category, cost, store_num) VALUES
(2001, 'Toothpaste', 50, 'Sensodyne Sensitivity & Gum Mint toothpaste is a dual action toothpaste thats specifically designed to help people with both sensitivity and early gum problems.', 
    'Personal Care', 1.99, 1),
(2002, 'Shampoo', 30, 'HARD WORKING, LONG LASTING Your haircare should work as hard as you do. Pantene Pro-V Daily Moisture Renewal Shampoo cleanses parched hair with a potent blend of nutrients to remove buildup and prime your strands for optimal hydration. ',
    'Personal Care', 3.99, 1),
(2003, 'Notebook', 100, ' Inside Pockets is an essential tool for school, work, or home. This one-subject notebook features 100 college-ruled sheets of heavyweight paper and inside pockets to help you organize handouts.',
    'Stationery', 2.49, 1),
(2004, '4K 55in TV', 20, 'Upgrade your home theater with this stylish 4K TV featuring vibrant colors, rich contrast and an advanced 4K processor.'
    'Electronics', 378.00, 20);

INSERT INTO supplies (supplier_id, barcode) VALUES 
(101, 2001),
(101, 2002),
(102, 2003),
(102, 2004);

INSERT INTO backorder (order_num, complete_date, start_date, quantity, employee_ssn, barcode, supplier_id, store_num) VALUES
(1, '2024-10-10', '2024-09-30', 10, '123456789', 1001, 101, 1),
(2, NULL, '2024-10-05', 5, '987654321', 1002, 102, 2);

