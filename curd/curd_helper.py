import mysql.connector
from datetime import datetime
import json

# Database Connection
def get_db_connection():
    """
    Establish a MySQL database connection.
    
    Returns:
        connection (mysql.connector.connection): MySQL connection object.
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="banking_system"
    )

# ---------------------------
# CRUD OPERATIONS
# ---------------------------

# ---- Customers ----
def create_customer(name, email, phone):
    """
    Create a new customer in the database.

    Args:
        name (str): Full name of the customer.
        email (str): Email address.
        phone (str): Phone number.

    Returns:
        int: ID of the created customer.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)",
        (name, email, phone)
    )
    conn.commit()
    customer_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return customer_id


def get_customer(customer_id):
    """
    Retrieve customer details by ID.

    Args:
        customer_id (int): Customer ID.

    Returns:
        dict: Customer details.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


# ---- Accounts ----
def create_account(customer_id, account_number, balance=0.0):
    """
    Create a new bank account.

    Args:
        customer_id (int): Customer ID.
        account_number (str): Unique account number.
        balance (float): Initial balance.

    Returns:
        int: Account ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO accounts (customer_id, account_number, balance) VALUES (%s, %s, %s)",
        (customer_id, account_number, balance)
    )
    conn.commit()
    account_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return account_id

def get_accounts_by_customer(customer_id):
    """
    Get all accounts for a given customer.

    Args:
        customer_id (int): Customer ID.

    Returns:
        list: List of accounts.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM accounts WHERE customer_id = %s", (customer_id,))
    accounts = cursor.fetchall()
    cursor.close()
    conn.close()
    return accounts

# ---- Transactions ----
def create_transaction(account_id, transaction_type, amount, description=""):
    """
    Create a transaction for an account.

    Args:
        account_id (int): Account ID.
        transaction_type (str): 'credit' or 'debit'.
        amount (float): Transaction amount.
        description (str): Transaction description.

    Returns:
        int: Transaction ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (account_id, transaction_type, amount, description) VALUES (%s, %s, %s, %s)",
        (account_id, transaction_type, amount, description)
    )

    # Update account balance
    if transaction_type == "credit":
        cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (amount, account_id))
    elif transaction_type == "debit":
        cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (amount, account_id))

    conn.commit()
    transaction_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return transaction_id

