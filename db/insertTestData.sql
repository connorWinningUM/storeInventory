INSERT INTO location (store_num, store_name, street_address, city, state, zip_code) VALUES
(1, 'Main Street Store', '123 Main St', 'Springfield', 'IL', 62704),
(2, 'Downtown Outlet', '456 Elm St', 'Chicago', 'IL', 60616);

INSERT INTO supplier (supplier_id, supplier_name, street_address, city, state, zip_code) VALUES
(101, 'Acme Supplies', '789 Oak St', 'Peoria', 'IL', 61614),
(102, 'Global Goods', '321 Pine St', 'Naperville', 'IL', 60540);

INSERT INTO employee (ssn, name, username, password, role, store_num) VALUES
('123456789', 'Alice Smith', 'asmith', 'password123', 'manager', 1),
('987654321', 'Bob Johnson', 'bjohnson', 'securepass', 'employee', 2);

INSERT INTO item (barcode, name, quantity, description, cost, store_num) VALUES
(1001, 'Widget A', 50, 'Standard widget', 9.99, 1),
(1002, 'Gadget B', 20, 'Deluxe gadget', 19.95, 2);

INSERT INTO backorder (order_num, complete_date, start_date, quantity, employee_ssn, barcode, supplier_id, store_num) VALUES
(1, '2024-10-10', '2024-09-30', 10, '123456789', 1001, 101, 1),
(2, NULL, '2024-10-05', 5, '987654321', 1002, 102, 2);

