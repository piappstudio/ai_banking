import json
from server import mcp

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
def transfer_funds(from_account_id, to_account_id, amount, description="Fund Transfer"):
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
        if balance < amount:
            raise ValueError("Insufficient funds.")

        create_transaction(from_account_id, "debit", amount, description)
        create_transaction(to_account_id, "credit", amount, description)
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print("Transfer failed:", e)
        return False
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

@mcp.tool()
def get_transaction_status(transaction_id):
    """
    Retrieve the status and details of a given transaction.

    Args:
        transaction_id (int): The unique ID of the transaction.

    Returns:
        dict: {
            "status": str,         # "completed" or "not found"
            "transaction": dict    # Transaction details if found
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
            "transaction": transaction
        }
    else:
        return {
            "status": "not found",
            "transaction": None
        }
