from flask import Flask, render_template, request, redirect, url_for
import cx_Oracle
from contextlib import contextmanager

app = Flask(__name__)

DB_USER = "bol"
DB_PASSWORD = "bol"
DB_DSN = "localhost/xe"


@contextmanager
def get_connection():
    conn = cx_Oracle.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
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
                "INSERT INTO STUDENTS (STUDENT_ID, NAME, EMAIL, PHONE) VALUES (:1, :2, :3, :4)",
                [student_id, name, email, phone]
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

                cursor.execute("SELECT item_id, item_name, price FROM menu_items WHERE item_id = :item_id", 
                               {'item_id': edit_item_id})
                edit_item = cursor.fetchone()


            if request.method == 'POST':
                item_id = request.form.get('edit_item_id')
                item_name = request.form['item_name']
                price = request.form['price']

                if item_id:  
                    
                    cursor.execute("UPDATE menu_items SET item_name = :item_name, price = :price WHERE item_id = :item_id", 
                                   {'item_name': item_name, 'price': price, 'item_id': item_id})
                else:  
                    
                    new_item_id = cursor.callfunc('add_menu_item', int, [item_name, price])

                    
                    cursor.execute("SELECT ITEM_ID_SEQ.CURRVAL FROM dual")
                    new_item_id = cursor.fetchone()[0]

                    
                    cursor.execute("INSERT INTO inventory (item_id, stock_level) VALUES (:item_id, 0)",
                                   {'item_id': new_item_id})  

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


            cursor.execute("DELETE FROM inventory WHERE item_id = :item_id", {'item_id': item_id})


            cursor.execute("DELETE FROM menu_items WHERE item_id = :item_id", {'item_id': item_id})


            conn.commit()

        return redirect(url_for('add_menu'))
    except Exception as e:
        print(f"Error deleting menu item: {e}")
        return "Error deleting menu item", 500


@app.route("/order_history")
def order_history():
    with get_connection() as conn:
        cursor = conn.cursor()
        ref_cursor = cursor.var(cx_Oracle.CURSOR)
        cursor.callproc("GetOrderHistory", [ref_cursor])

        orders = ref_cursor.getvalue().fetchall()
    return render_template("order_history.html",orders=orders)

@app.route("/toggle_payment/<int:order_id>")
def toggle_payment(order_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT STATUS FROM PAYMENT WHERE ORDER_ID = :1", [order_id])
        current_status = cursor.fetchone()[0]
        new_status = "Completed" if current_status == "Pending" else "Pending"
        cursor.execute("UPDATE PAYMENT SET STATUS = :1 WHERE ORDER_ID = :2", [new_status, order_id])
        conn.commit()
    return redirect(url_for('order_history'))

@app.route('/inventory', methods=['GET'])
def inventory():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            
            ref_cursor = cursor.var(cx_Oracle.CURSOR)
            cursor.callproc('get_inventory_data', [ref_cursor])

            
            inventory_items = ref_cursor.getvalue().fetchall()

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

            
            print(f"Updating item_id: {item_id} with stock_level: {stock_level}")

            
            result = cursor.callfunc('update_inventory_stock', str, [item_id, stock_level])

            
            print(f"Function result: {result}")

            if result == 'Item not found':
                return f"Item with ID {item_id} not found.", 404

            
            conn.commit()

        
        return redirect('/inventory')

    except Exception as e:
        
        print(f"Error updating inventory: {e}")
        return f"Error: {e}",500



if __name__ == '__main__':
    app.run(debug=True)
