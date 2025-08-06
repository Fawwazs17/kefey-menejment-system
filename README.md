# IIUM Cafe Management System

This project is a simple web-based application for managing a cafe, likely within the International Islamic University Malaysia (IIUM). It allows for the management of students, menu items, inventory, and order history.

## Features

*   **Student Management:** Add and view student information.
*   **Menu Management:** Add, edit, and delete menu items and their prices.
*   **Inventory Management:** Track the stock levels of menu items and update them.
*   **Order History:** View a history of all orders and toggle their payment status.

## Technologies Used

*   **Backend:** Python (Flask)
*   **Database:** Oracle Database (`cx_Oracle` driver)
*   **Frontend:** HTML, CSS, JavaScript

## Setup and Installation

To run this application, you will need to have Python and an Oracle Database instance installed.

### 1. Database Setup

1.  **Connect to your Oracle Database:**
    ```sql
    sqlplus your_username/your_password@your_tns_alias
    ```

2.  **Create the necessary tables:**
    You will need to create the following tables: `STUDENTS`, `MENU_ITEMS`, `INVENTORY`, `ORDERS`, and `PAYMENT`. The exact schema can be inferred from the queries in `app.py`.

3.  **Create the necessary stored procedures and functions:**
    The application uses several stored procedures and functions (`add_menu_item`, `GetOrderHistory`, `get_inventory_data`, `update_inventory_stock`). You will need to create these in your database. The logic for these procedures should align with the application's functionality.

4.  **Create the sequence for menu item IDs:**
    ```sql
    CREATE SEQUENCE ITEM_ID_SEQ;
    ```

### 2. Application Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install the required Python packages:**
    ```bash
    pip install Flask cx_Oracle
    ```

3.  **Configure the database connection:**
    Open `app.py` and update the following variables with your Oracle Database credentials:
    ```python
    DB_USER = "your_username"
    DB_PASSWORD = "your_password"
    DB_DSN = "your_tns_alias" # e.g., "localhost/xe"
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```

The application will be available at `http://127.0.0.1:5000`.
