import sqlite3

conn = sqlite3.connect('reservation.db')
cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS Reservations;
DROP TABLE IF EXISTS RestaurantTables;
DROP TABLE IF EXISTS Customers;

CREATE TABLE Customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    email TEXT
);

CREATE TABLE RestaurantTables (
    table_id INTEGER PRIMARY KEY AUTOINCREMENT,
    capacity INTEGER,
    location TEXT
);

CREATE TABLE Reservations (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    table_id INTEGER,
    reservation_date DATE,
    reservation_time TIME,
    num_guests INTEGER,
    status TEXT DEFAULT 'active',
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (table_id) REFERENCES RestaurantTables(table_id)
);

INSERT INTO RestaurantTables (capacity, location) VALUES
(2, 'Indoor'), (4, 'Indoor'), (6, 'Outdoor'), (8, 'VIP');
""")

conn.commit()
conn.close()
print("Database initialized!")