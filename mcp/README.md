# AI Banking MCP Server

A Model Context Protocol (MCP) server that provides secure, AI-powered banking assistance. This server interfaces with the AI Banking Laravel backend to manage accounts, transactions with 2FA, and payee management.

## Features

- **Authentication:** Secure login via email/password or manual Bearer token.
- **Account Management:** Real-time balances and details for multiple bank accounts.
- **Secure Transfers:** Two-step fund transfers with 6-digit email verification codes.
- **Transaction Analytics:** Historical data analysis and budget tracking.
- **Security Protocols:** Built-in guardrails for PII protection and data masking.

## Prerequisites

- **Python 3.12+**
- **uv** (Modern Python package manager)
- **AI Banking Laravel Server** (running at `http://localhost:8000`)

### Installation & Setup

1. **Install `uv`** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Initialize and sync dependencies**:
   ```bash
   cd mcp
   uv sync
   ```

3. **Run the server locally**:
   ```bash
   uv run main.py
   ```

### 1. Visual Studio Code (Claude Dev / Roo Code)

If you are using an extension like **Roo Code** or **Claude Dev**, add the following to your `settings.json` or MCP configuration:

```json
{
  "mcpServers": {
    "ai-banking": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/apple/LLM/ai_banking/mcp",
        "run",
        "main.py"
      ]
    }
  }
}
```

### 2. Android Studio (Gemini / AI Plugin)

To use this with Android Studio's AI capabilities:
1. Ensure the `uv` is installed on your system.
2. In the AI Settings, add a new MCP server.
3. Command: `uv`
4. Args: `--directory /Users/apple/LLM/ai_banking/mcp run main.py`

### 3. Claude Desktop App

Add the following to your Claude Desktop configuration file (usually found at `~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "ai-banking": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/apple/LLM/ai_banking/mcp",
        "run",
        "main.py"
      ]
    }
  }
}
```

---

## Available Tools

| Tool | Description |
| :--- | :--- |
| `login` | Authenticate using email and password. |
| `set_bearer_token` | Manually set an existing API token. |
| `get_customer_summary` | Overview of all accounts and balances. |
| `make_transfer_funds` | **Step 1:** Initiate a transfer (triggers email code). |
| `authorize_transfer` | **Step 2:** Complete transfer with 6-digit code. |
| `get_transactions` | Fetch history for a specific account. |
| `get_transaction_analytics`| View spending and income trends. |
| `get_security_protocol` | Check system protection details. |

---

## Security Guardrails

This MCP server is built with **Banking Assistance Principles**:
1. **Masking:** Full account numbers are never displayed in raw form.
2. **PII Protection:** Personally Identifiable Information is strictly managed.
3. **No Advice:** The assistant provides data and execution, never financial advice.
4. **Enforced 2FA:** No fund movements occur without secondary email verification.

## Development

To test the server locally:
```bash
python3 mcp/main.py
```
