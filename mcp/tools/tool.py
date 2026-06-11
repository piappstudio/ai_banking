import json
import requests
from app import mcp
from decimal import Decimal

from typing import Optional

# ---------------------------
# API CONFIGURATION
# ---------------------------
BASE_URL = "http://localhost:8000/api/v1"
SESSION_TOKEN = None

@mcp.tool()
def login(email: str, password: str):
    """
    Authenticate with the AI Banking system using email and password.
    
    Args:
        email (str): User's email address.
        password (str): User's password.
        
    Returns:
        str: Success message or error.
    """
    global SESSION_TOKEN
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": email,
            "password": password
        })
        if response.status_code == 200:
            SESSION_TOKEN = response.json()['data']['token']
            return "Login successful. Session token updated."
        else:
            return f"Login failed: {response.json().get('message', 'Invalid credentials')}"
    except Exception as e:
        return f"Authentication error: {str(e)}"

@mcp.tool()
def set_bearer_token(token):
    """
    Manually set a Bearer token for the current session.
    
    Args:
        token (str): The plain-text token from a previous login or signup.
        
    Returns:
        str: Success message.
    """
    global SESSION_TOKEN
    SESSION_TOKEN = token
    return "Bearer token updated for the current session."

def api_request(method, endpoint, data=None, params=None):
    """Helper to make authenticated API requests."""
    if not SESSION_TOKEN:
        return {"error": "Authentication required. Please call 'login' or 'set_bearer_token' first.", "status": 401}
        
    headers = {"Authorization": f"Bearer {SESSION_TOKEN}", "Accept": "application/json"}
    
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            return {"error": f"Unsupported method: {method}"}
            
        if response.status_code >= 400:
            return {"error": response.json().get('message', 'API request failed'), "status": response.status_code}
            
        return response.json().get('data')
    except Exception as e:
        return {"error": f"Network error: {str(e)}"}

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
def make_transfer_funds(from_account_id: int, to_account_id: int = None, to_payee_id: int = None, amount: float = 0, description: str = "Fund Transfer"):
    """
    Initiate a fund transfer between accounts or to a saved payee. 
    Note: This will send a 6-digit code to the user's email.
    The user must then call authorize_transfer with the verification_id and code.

    Args:
        from_account_id (int): Source account ID.
        to_account_id (int): Destination account ID (optional if to_payee_id is provided).
        to_payee_id (int): Destination payee ID (optional if to_account_id is provided).
        amount (float): Transfer amount.
        description (str): Description.

    Returns:
        str: Result message with verification_id.
    """
    data = {
        "from_account_id": from_account_id,
        "amount": float(amount),
        "description": description
    }
    if to_account_id is not None:
        data["to_account_id"] = to_account_id
    if to_payee_id is not None:
        data["to_payee_id"] = to_payee_id
    
    result = api_request("POST", "/transactions/transfer", data=data)
    
    if "error" in result:
        return f"Transfer initiation failed: {result['error']}"
        
    verification_msg = f"Transfer initiated. Verification ID: {result['verification_id']}. Code sent to email."
    
    return verification_msg

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
        "greetings": "Welcome to AI Banking Secure Assistant",
        "message": "I can help you manage your accounts, view transactions, and initiate secure transfers. All transactions require two-step verification for your safety."
    }

@mcp.prompt()
def banking_assistant_prompt(query: str) -> str:
    """
    Standard banking assistant prompt with security guardrails.
    """
    return f"""
    You are the AI Banking Secure Assistant. Your primary goal is to help users manage their finances safely and efficiently.

    ### CORE PRINCIPLES & SECURITY GUARDRAILS:
    1. **Confidentiality:** NEVER display full account numbers (mask them as ****1234). NEVER leak Personally Identifiable Information (PII) like full addresses or phone numbers unless absolutely necessary for a specific confirmation step.
    2. **Two-Step Authorization:** Always inform the user that transfers are initiated in two steps:
       - Step 1: Initiation (triggers a 6-digit code to their email).
       - Step 2: Authorization (user must provide the code to complete the transfer).
    3. **No Financial Advice:** You are a banking assistant, not a financial advisor. Do not provide investment advice or predict market trends.
    4. **Precision:** Always use the provided tools to fetch real-time balances and transaction history. Do not guess or hallucinate financial data.
    5. **Clarity:** Use professional, clear, and concise language. If a transaction fails, explain the reason clearly (e.g., insufficient funds).

    User Query: {query}
    """

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
def get_security_protocol():
    """
    Retrieve information about the system's security and protection protocols.
    """
    return {
        "encryption": "Industry-standard AES-256 for data at rest, TLS 1.3 for data in transit.",
        "authentication": "Secure token-based authentication (Laravel Sanctum).",
        "authorization": "Two-step verification for all fund movements using 6-digit email codes.",
        "privacy": "Strict adherence to data minimization principles. PII is masked in all UI views.",
        "monitoring": "Real-time transaction monitoring and anomaly detection."
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

@mcp.tool()
def add_payee(nickname, account_number=None, routing_number=None, phone_number=None, email=None, address=None):
    """
    Add a new payee to the user's account.

    Args:
        nickname (str): A nickname for the payee.
        account_number (str): Optional account number.
        routing_number (str): Optional routing number.
        phone_number (str): Optional phone number (for Zelle).
        email (str): Optional email address.
        address (str): Optional physical address.

    Returns:
        str: Success message or error.
    """
    data = {
        "nickname": nickname,
        "accountNumber": account_number,
        "routingNumber": routing_number,
        "phoneNumber": phone_number,
        "email": email,
        "address": address
    }
    # Filter out None values
    data = {k: v for k, v in data.items() if v is not None}
    
    result = api_request("POST", "/payees", data=data)
    
    if "error" in result:
        return f"Failed to add payee: {result['error']}"
        
    return f"Payee '{nickname}' added successfully."

@mcp.tool()
def list_payees():
    """
    List all saved payees for the authenticated user.

    Returns:
        str: JSON string containing the list of payees.
    """
    payees = api_request("GET", "/payees")
    if "error" in payees:
        return json.dumps(payees)
        
    return json.dumps(payees, default=str)
