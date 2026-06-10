import json
from curd.curd_helper import get_db_connection, get_customer, get_accounts_by_customer, create_transaction
from server import mcp
from decimal import Decimal


# ---------------------------
# ABSTRACT BANKING FUNCTIONS
# ---------------------------

# @mcp.route("/customer/<int:customer_id>/summary", methods=["GET"])
# @mcp.auth_required
@mcp.tool()
def get_customer_summary(customer_id):
    """
    Get logged-in customer summary in JSON.

    Args:
        customer_id (int): Customer ID.

    Returns:
        str: JSON string containing customer info, account count, and recent transactions.
    """
    customer = get_customer(customer_id)
    accounts = get_accounts_by_customer(customer_id)
    summary = {
        "customer": customer,
        "number_of_accounts": len(accounts),
        "accounts": accounts
    }
    return json.dumps(summary, default=str)


# @mcp.route("/customer/<int:customer_id>/accounts", methods=["GET"])
# @mcp.auth_required
@mcp.tool()
def make_transfer_funds(from_account_id, to_account_id, amount, description="Fund Transfer"):
    """
    Transfer funds from one account to another.

    Args:
        from_account_id (int): Source account ID.
        to_account_id (int): Destination account ID.
        amount (float): Transfer amount.
        description (str): Description.

    Returns:
        bool: True if success, False otherwise.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (from_account_id,))
        balance = cursor.fetchone()[0]
        if float(balance) < float(amount):
            raise ValueError("Insufficient funds.")

        create_transaction(from_account_id, "debit", amount, description)
        create_transaction(to_account_id, "credit", amount, description)
        conn.commit()
        return(f"Transfer of {amount} from account {from_account_id} to {to_account_id} successful.")
    except Exception as e:
        conn.rollback()
        return(f"Transfer failed:", e)

    finally:
        cursor.close()
        conn.close()


# @mcp.route("/account/<int:account_id>/transactions", methods=["GET"])
# @mcp.auth_required
@mcp.tool()
def get_transactions(account_id, start_date=None, end_date=None):
    """
    Retrieve transactions for an account.

    Args:
        account_id (int): Account ID.
        start_date (str): Optional. Format 'YYYY-MM-DD'.
        end_date (str): Optional. Format 'YYYY-MM-DD'.

    Returns:
        list: Transactions.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if start_date and end_date:
        cursor.execute(
            "SELECT * FROM transactions WHERE account_id = %s AND DATE(created_at) BETWEEN %s AND %s ORDER BY created_at DESC",
            (account_id, start_date, end_date)
        )
    else:
        cursor.execute(
            "SELECT * FROM transactions WHERE account_id = %s ORDER BY created_at DESC LIMIT 100",
            (account_id,)
        )
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()
    return transactions

# Basic dynamic resource returning a string
@mcp.resource("resource://greeting")
def get_greeting():
    """Provides a simple greeting message."""
    return "Hello from FastMCP Resources!"

@mcp.resource("data://config")
def get_config() -> dict:
    """Provides the application configuration."""
    return {"theme": "dark", "version": "1.0"}


@mcp.tool()
def get_welcome_message():
    return {
        "greetings": "Welcome to Pi AI Banking",
    }

@mcp.prompt()
def code_review_prompt(question:str) -> str:
    """Android question prompt"""
    return f""" Consider youself andorid software engineer, now, answer : {question} """

@mcp.tool()
def get_transaction_status(transaction_id):
    """
    Retrieve the status and details of a given transaction.
    Use template://transaction to visualize the transaction data.

    Args:
        transaction_id (int): The unique ID of the transaction.

    Returns:
        dict: {
            "status": str,                    # "completed" or "not found"
            "transaction": dict,              # Transaction details if found
            "template_uri": str               # Resource URI for visualization
        }
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transactions WHERE transaction_id = %s", (transaction_id,))
    transaction = cursor.fetchone()
    cursor.close()
    conn.close()

    if transaction:
        return {
            "status": "completed",
            "transaction": transaction,
            "template_uri": "template://transaction",
            "visualization_hint": "Use the transaction template to display this data"
        }
    else:
        return {
            "status": "not found",
            "transaction": None,
            "template_uri": "template://transaction"
        }


@mcp.tool()
def get_home_dashboard(customer_id):
    """
    Get customer dashboard data for home screen visualization.
    Use template://home to display the dashboard.

    Args:
        customer_id (int): Customer ID.

    Returns:
        dict: Dashboard data with template reference
    """
    customer = get_customer(customer_id)
    accounts = get_accounts_by_customer(customer_id)
    
    return {
        "customer": customer,
        "accounts": accounts,
        "template_uri": "template://home",
        "visualization_hint": "Load template://home to render this dashboard"
    }


@mcp.tool()
def get_transaction_analytics(account_id, start_date=None, end_date=None):
    """
    Get transaction analytics and budget data.
    Use template://transaction to visualize the analytics.

    Args:
        account_id (int): Account ID.
        start_date (str): Optional. Format 'YYYY-MM-DD'.
        end_date (str): Optional. Format 'YYYY-MM-DD'.

    Returns:
        dict: Analytics data with template reference
    """
    transactions = get_transactions(account_id, start_date, end_date)
    
    total_spent = sum(float(t.get('amount', 0)) for t in transactions if t.get('type') == 'debit')
    total_received = sum(float(t.get('amount', 0)) for t in transactions if t.get('type') == 'credit')
    
    return {
        "transactions": transactions,
        "analytics": {
            "total_spent": total_spent,
            "total_received": total_received,
            "transaction_count": len(transactions)
        },
        "template_uri": "template://transaction",
        "visualization_hint": "Use template://transaction to display analytics and budget breakdown"
    }


@mcp.tool()
def get_user_menu(customer_id):
    """
    Get user profile and menu data.
    Use template://menu to display the profile and navigation.

    Args:
        customer_id (int): Customer ID.

    Returns:
        dict: Profile data with template reference
    """
    customer = get_customer(customer_id)
    accounts = get_accounts_by_customer(customer_id)
    
    return {
        "profile": customer,
        "accounts": accounts,
        "menu_items": [
            {"section": "Account", "items": ["Home", "Transaction", "Wallet", "Card"]},
            {"section": "Settings", "items": ["Settings", "Security", "Support", "Terms & Privacy"]},
            {"section": "Profile", "items": ["Edit Profile", "Preferences", "Logout"]}
        ],
        "template_uri": "template://menu",
        "visualization_hint": "Load template://menu to render the profile and menu"
    }
