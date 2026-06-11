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
- **ngrok** (optional, for remote SSE transport)

## Authentication (Fixing "Security Guardrails")

If your AI assistant refuses to accept passwords or tokens in chat, you can provide the token via an environment variable or a `.env` file:

1. Create a `.env` file in the `mcp/` directory (copy from `.env.example`).
2. Add your token: `BANKING_SESSION_TOKEN=your_token_here`.
3. Restart the MCP server.

Alternatively, set the `BANKING_SESSION_TOKEN` environment variable in your MCP configuration file.

## Installation & Setup

1. **Install `uv`** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Initialize and sync dependencies**:
   ```bash
   cd mcp
   uv sync
   ```

## Transport Modes

The server supports two transport modes: **Local (stdio)** and **Remote (SSE)**.

### 1. Local / Studio Mode (Default)
Used for local integration with IDEs (Android Studio, VS Code) or Claude Desktop. The server communicated via standard input/output.

**Run command:**
```bash
uv run main.py
```

#### Android Studio (Gemini / AI Plugin)
1. In the AI Settings, add a new MCP server.
2. **Command:** `uv`
3. **Args:** `--directory /Users/apple/LLM/ai_banking/mcp run main.py`
4. **Environment Variables**: Add `BANKING_SESSION_TOKEN` with your Bearer token.

#### Visual Studio Code (Roo Code / Claude Dev)
Add to your `settings.json`:
```json
{
  "mcpServers": {
    "ai-banking": {
      "command": "uv",
      "args": ["--directory", "/Users/apple/LLM/ai_banking/mcp", "run", "main.py"],
      "env": {
        "BANKING_SESSION_TOKEN": "your_actual_token_here"
      }
    }
  }
}
```

### 2. Remote / SSE Mode
Used to expose the server over HTTP, typically via a tunnel like ngrok for remote AI access.

**Run command (starts on port 4001):**
```bash
uv run main.py --sse
```

**Expose via ngrok:**
```bash
ngrok http 4001
```

**Connect URL:**
`https://mystified-uncloak-effects.ngrok-free.dev/sse`

> **Note on Authentication:** In Remote/SSE mode, the `BANKING_SESSION_TOKEN` must be set as an environment variable on the **machine running the server**. The remote client does not need to provide the token in its configuration.

#### Configuration for Remote Clients

**Claude Desktop:**
Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "ai-banking": {
      "command": "uv",
      "args": ["--directory", "/Users/apple/LLM/ai_banking/mcp", "run", "main.py"],
      "env": {
        "BANKING_SESSION_TOKEN": "your_actual_token_here"
      }
    }
  }
}
```

**Android Studio (AI Plugin):**
1. Select **SSE** transport type.
2. **URL:** `https://mystified-uncloak-effects.ngrok-free.dev/sse`

**VS Code (Roo Code / Claude Dev):**
Add to `settings.json`:
```json
{
  "mcpServers": {
    "ai-banking-remote": {
      "url": "https://mystified-uncloak-effects.ngrok-free.dev/sse"
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
| `add_payee` | Add a new banking contact or Zelle payee. |
| `list_payees` | View all saved payees. |

---

## Security Guardrails

This MCP server is built with **Banking Assistance Principles**:
1. **Masking:** Full account numbers are never displayed in raw form.
2. **PII Protection:** Personally Identifiable Information is strictly managed.
3. **No Advice:** The assistant provides data and execution, never financial advice.
4. **Enforced 2FA:** No fund movements occur without secondary email verification.
