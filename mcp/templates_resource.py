"""
MCP Resources for Banking App UI Templates
Exposes HTML templates as resources for use in Claude
"""

import os
from pathlib import Path
from server import mcp

# Get the templates directory path
TEMPLATES_DIR = Path(__file__).parent / "templates"


@mcp.resource("template://home")
def get_home_template() -> str:
    """Get the Home screen HTML template showing account balance and recent transactions."""
    template_path = TEMPLATES_DIR / "home.html"
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


@mcp.resource("template://transaction")
def get_transaction_template() -> str:
    """Get the Transaction screen HTML template showing card transactions and monthly budget."""
    template_path = TEMPLATES_DIR / "transaction.html"
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


@mcp.resource("template://menu")
def get_menu_template() -> str:
    """Get the Menu screen HTML template showing user profile and navigation items."""
    template_path = TEMPLATES_DIR / "menu.html"
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


@mcp.resource("template://list")
def list_all_templates() -> str:
    """List all available UI templates."""
    templates = {
        "home": "Home screen - Shows account balance, card details, and recent transactions",
        "transaction": "Transaction screen - Displays card transactions and monthly budget analysis",
        "menu": "Menu screen - User profile and navigation menu for app features",
    }
    
    return (
        "Available Banking App UI Templates:\n\n"
        + "\n".join(f"- {name}: {desc}" for name, desc in templates.items())
        + "\n\nAccess templates using: template://{name}"
    )


# ---------------------------
# MCP TOOLS - Force Resource URI Usage
# ---------------------------

@mcp.tool()
def get_ui_template(screen_name: str) -> str:
    """
    Get a UI template by screen name. Forces use of resource URIs.
    
    Args:
        screen_name (str): One of 'home', 'transaction', or 'menu'
    
    Returns:
        str: Resource URI reference or template content
    """
    resource_map = {
        "home": "template://home",
        "transaction": "template://transaction",
        "menu": "template://menu",
        "list": "template://list"
    }
    
    if screen_name.lower() in resource_map:
        uri = resource_map[screen_name.lower()]
        return f"Template available at: {uri}\n\nUse the resource URI directly to fetch the HTML content."
    return f"Unknown screen: {screen_name}. Available options: home, transaction, menu"


@mcp.tool()
def render_template(template_type: str) -> str:
    """
    Render and return a complete template with enforced resource reference.
    
    Args:
        template_type (str): Template type - 'home', 'transaction', or 'menu'
    
    Returns:
        str: Complete HTML template content
    """
    template_map = {
        "home": get_home_template,
        "transaction": get_transaction_template,
        "menu": get_menu_template,
    }
    
    if template_type.lower() in template_map:
        return template_map[template_type.lower()]()
    return f"Template '{template_type}' not found. Use 'home', 'transaction', or 'menu'."
