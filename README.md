# IIUM Cafe Management System

This project is a simple web-based application for managing a cafe, likely within the International Islamic University Malaysia (IIUM). It allows for the management of students, menu items, inventory, and order history.

## Features

*   **Student Management:** Add and view student information.
*   **Menu Management:** Add, edit, and delete menu items and their prices.
*   **Inventory Management:** Track the stock levels of menu items and update them.
*   **Order History:** View a history of all orders and toggle their payment status.

## Technologies Used

*   **Backend:** Python (Flask)
*   **Database:** SQLite
*   **Frontend:** HTML, CSS, JavaScript

## Setup and Installation

To run this application, you will need to have Python installed.

### 1. Application Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install the required Python packages:**
    ```bash
    pip install Flask
    ```

### 2. Database Setup

1.  **Run the database setup script:**
    This will create a `database.db` file in the project directory with all the necessary tables and sample data.
    ```bash
    python database_setup.py
    ```

### 3. Run the application

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`.
