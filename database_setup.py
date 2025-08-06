import sqlite3

def setup_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create STUDENTS table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS STUDENTS (
        STUDENT_ID TEXT PRIMARY KEY,
        NAME TEXT NOT NULL,
        EMAIL TEXT NOT NULL,
        PHONE TEXT NOT NULL
    )
    ''')

    # Create menu_items table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu_items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        price REAL NOT NULL
    )
    ''')

    # Create inventory table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        item_id INTEGER,
        stock_level INTEGER NOT NULL,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
    )
    ''')

    # Create orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        payment_method TEXT,
        total REAL
    )
    ''')

    # Create payment table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS payment (
        order_id INTEGER,
        status TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    )
    ''')

    # Insert some sample data
    cursor.execute("INSERT INTO menu_items (item_name, price) VALUES ('Nasi Lemak', 5.50)")
    cursor.execute("INSERT INTO inventory (item_id, stock_level) VALUES (1, 50)")
    cursor.execute("INSERT INTO menu_items (item_name, price) VALUES ('Mee Goreng', 6.00)")
    cursor.execute("INSERT INTO inventory (item_id, stock_level) VALUES (2, 30)")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()
    print("Database has been set up successfully.")
