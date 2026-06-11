import json
import requests
from mcp.server import mcp
from decimal import Decimal

# ---------------------------
# API CONFIGURATION
# ---------------------------
BASE_URL = "http://localhost:8000/api/v1"
AUTH_TOKEN = None

def get_auth_token():
    """
    Authenticate with the API and get a token.
    In a real scenario, this would use secure credentials.
    """
    global AUTH_TOKEN
    if AUTH_TOKEN:
        return AUTH_TOKEN
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "rajesh@example.com",
            "password": "SecurePass123"
        })
        if response.status_code == 200:
            AUTH_TOKEN = response.json()['data']['token']
            return AUTH_TOKEN
    except Exception as e:
        print(f"Auth failed: {e}")
    return None

def api_request(method, endpoint, data=None, params=None):
    """Helper to make authenticated API requests."""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    url = f"{BASE_URL}{endpoint}"
    
    if method == "GET":
        response = requests.get(url, headers=headers, params=params)
    elif method == "POST":
        response = requests.post(url, headers=headers, json=data)
    else:
        return None
        
    if response.status_code >= 400:
        return {"error": response.json().get('message', 'API request failed'), "status": response.status_code}
        
    return response.json().get('data')

# ---------------------------
# ABSTRACT BANKING FUNCTIONS
# ---------------------------

@mcp.tool()
def get_customer_summary(customer_id=None):
    """
    Get logged-in customer summary in JSON.

    Returns:
        str: JSON string containing accounts and balances.
    """
    accounts = api_request("GET", "/accounts")
    if "error" in accounts:
        return json.dumps(accounts)
        
    summary = {
        "number_of_accounts": len(accounts),
        "accounts": accounts
    }
    return json.dumps(summary, default=str)


@mcp.tool()
def make_transfer_funds(from_account_id, to_account_id, amount, description="Fund Transfer"):
    """
    Initiate a fund transfer between accounts. 
    Note: This will send a 6-digit code to the user's email.
    The user must then call authorize_transfer with the verification_id and code.

    Args:
        from_account_id (int): Source account ID.
        to_account_id (int): Destination account ID.
        amount (float): Transfer amount.
        description (str): Description.

    Returns:
        str: Result message with verification_id.
    """
    data = {
        "from_account_id": from_account_id,
        "to_account_id": to_account_id,
        "amount": float(amount),
        "description": description
    }
    
    result = api_request("POST", "/transactions/transfer", data=data)
    
    if "error" in result:
        return f"Transfer initiation failed: {result['error']}"
        
    return f"Transfer initiated. Verification ID: {result['verification_id']}. Code sent to email."

@mcp.tool()
def authorize_transfer(verification_id, code):
    """
    Authorize and complete a pending transfer using the 6-digit code.

    Args:
        verification_id (int): Verification ID from transfer initiation.
        code (str): 6-digit code sent to email.

    Returns:
        str: Success or failure message.
    """
    data = {
        "verification_id": verification_id,
        "code": code
    }
    
    result = api_request("POST", "/transactions/authorize", data=data)
    
    if "error" in result:
        return f"Authorization failed: {result['error']}"
        
    return "Transfer completed successfully."


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
    params = {}
    if start_date: params['start_date'] = start_date
    if end_date: params['end_date'] = end_date
    
    transactions = api_request("GET", f"/accounts/{account_id}/transactions", params=params)
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
        "greetings": "Welcome to AI Banking MCP",
    }

@mcp.prompt()
def code_review_prompt(question:str) -> str:
    """Android question prompt"""
    return f""" Consider youself andorid software engineer, now, answer : {question} """

@mcp.tool()
def get_transaction_status(transaction_id):
    """
    Retrieve the status and details of a given transaction.
    (Note: Currently implemented via transaction list search)

    Args:
        transaction_id (int): The unique ID of the transaction.

    Returns:
        dict: Transaction details or error.
    """
    # In a full implementation, we'd have a specific /transactions/{id} endpoint
    # For now, we'll return a placeholder or search.
    return {
        "status": "Search feature coming soon",
        "transaction_id": transaction_id,
        "template_uri": "template://transaction"
    }


@mcp.tool()
def get_home_dashboard(customer_id=None):
    """
    Get customer dashboard data for home screen visualization.
    Use template://home to display the dashboard.

    Returns:
        dict: Dashboard data with template reference
    """
    accounts = api_request("GET", "/accounts")
    
    return {
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

    Returns:
        dict: Analytics data with template reference
    """
    transactions = get_transactions(account_id, start_date, end_date)
    
    if "error" in transactions:
        return transactions
        
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
def get_user_menu(customer_id=None):
    """
    Get user profile and menu data.
    Use template://menu to display the profile and navigation.

    Returns:
        dict: Profile data with template reference
    """
    accounts = api_request("GET", "/accounts")
    
    return {
        "accounts": accounts,
        "menu_items": [
            {"section": "Account", "items": ["Home", "Transaction", "Wallet", "Card"]},
            {"section": "Settings", "items": ["Settings", "Security", "Support", "Terms & Privacy"]},
            {"section": "Profile", "items": ["Edit Profile", "Preferences", "Logout"]}
        ],
        "template_uri": "template://menu",
        "visualization_hint": "Load template://menu to render the profile and menu"
    }
