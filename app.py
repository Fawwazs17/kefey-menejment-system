from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from contextlib import contextmanager

app = Flask(__name__)

DB_NAME = "database.db"

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

@app.route("/")
def home():
    return redirect(url_for('add_student'))

@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    with get_connection() as conn:
        cursor = conn.cursor()
        if request.method == "POST":
            student_id = request.form["student_id"]
            name = request.form["name"]
            email = request.form["email"]
            phone = request.form["phone"]
            cursor.execute(
                "INSERT INTO STUDENTS (STUDENT_ID, NAME, EMAIL, PHONE) VALUES (?, ?, ?, ?)",
                (student_id, name, email, phone)
            )
            conn.commit()
        cursor.execute("SELECT * FROM STUDENTS")
        students = cursor.fetchall()
    return render_template("add_student.html", students=students)

@app.route('/add_menu', methods=['GET', 'POST'])
def add_menu():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT item_id, item_name, price FROM menu_items")
            menu_items = cursor.fetchall()

            edit_item = None
            edit_item_id = request.args.get('edit_item_id')
            if edit_item_id:
                cursor.execute("SELECT item_id, item_name, price FROM menu_items WHERE item_id = ?",
                               (edit_item_id,))
                edit_item = cursor.fetchone()

            if request.method == 'POST':
                item_id = request.form.get('edit_item_id')
                item_name = request.form['item_name']
                price = request.form['price']

                if item_id:
                    cursor.execute("UPDATE menu_items SET item_name = ?, price = ? WHERE item_id = ?",
                                   (item_name, price, item_id))
                else:
                    cursor.execute("INSERT INTO menu_items (item_name, price) VALUES (?, ?)", (item_name, price))
                    new_item_id = cursor.lastrowid
                    cursor.execute("INSERT INTO inventory (item_id, stock_level) VALUES (?, 0)", (new_item_id,))

                conn.commit()
                return redirect(url_for('add_menu'))

        return render_template('add_menu.html', menu_items=menu_items, edit_item=edit_item)

    except Exception as e:
        print(f"Error: {e}")
        return f"An error occurred: {e}", 500

@app.route('/delete_menu/<int:item_id>', methods=['GET'])
def delete_menu(item_id):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM inventory WHERE item_id = ?", (item_id,))
            cursor.execute("DELETE FROM menu_items WHERE item_id = ?", (item_id,))
            conn.commit()

        return redirect(url_for('add_menu'))
    except Exception as e:
        print(f"Error deleting menu item: {e}")
        return "Error deleting menu item", 500

@app.route("/order_history")
def order_history():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT o.order_id, o.order_time, o.payment_method, p.status, o.total
            FROM orders o
            JOIN payment p ON o.order_id = p.order_id
        """)
        orders = cursor.fetchall()
    return render_template("order_history.html", orders=orders)

@app.route("/toggle_payment/<int:order_id>")
def toggle_payment(order_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT STATUS FROM PAYMENT WHERE ORDER_ID = ?", (order_id,))
        current_status = cursor.fetchone()[0]
        new_status = "Completed" if current_status == "Pending" else "Pending"
        cursor.execute("UPDATE PAYMENT SET STATUS = ? WHERE ORDER_ID = ?", (new_status, order_id))
        conn.commit()
    return redirect(url_for('order_history'))

@app.route('/inventory', methods=['GET'])
def inventory():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT mi.item_id, mi.item_name, i.stock_level, i.last_updated
                FROM menu_items mi
                JOIN inventory i ON mi.item_id = i.item_id
            """)
            inventory_items = cursor.fetchall()
        return render_template('inventory.html', inventory_items=inventory_items)
    except Exception as e:
        print(f"Error fetching inventory data: {e}")
        return "Error fetching inventory data"

@app.route('/update_inventory', methods=['POST'])
def update_inventory():
    item_id = request.form['item_id']
    stock_level = request.form['stock_level']

    try:
        stock_level = int(stock_level)
    except ValueError:
        return "Invalid stock level", 400

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE inventory SET stock_level = ?, last_updated = CURRENT_TIMESTAMP WHERE item_id = ?",
                           (stock_level, item_id))
            conn.commit()
        return redirect('/inventory')
    except Exception as e:
        print(f"Error updating inventory: {e}")
        return f"Error: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
