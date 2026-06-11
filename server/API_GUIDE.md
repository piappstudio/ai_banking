# AI Banking API Documentation

This project provides a comprehensive banking API with secure authentication and multi-step transaction authorization.

## Base URL
`http://localhost:8000`

## Postman Setup
1. Import `AI_Banking_API.postman_collection.json` into Postman.
2. Import `AI_Banking_Environment.postman_environment.json` into Postman.
3. Select the `AI Banking Local` environment.

## API Modules

### 1. Authentication (Public)
*   **Signup**: `POST /api/v1/auth/signup` - Create a new account.
*   **Login**: `POST /api/v1/auth/login` - Authenticate and get a Bearer token.
*   **Verify Email**: `POST /api/v1/auth/verify-email` - Confirm registration with a 6-digit code.
*   **Forgot/Reset Password**: Complete flow for password recovery.

### 2. Accounts (Protected)
*   **List Accounts**: `GET /api/v1/accounts` - View all your accounts and balances.
*   **Account Details**: `GET /api/v1/accounts/{id}` - View specific account info.
*   **Transactions History**: `GET /api/v1/accounts/{id}/transactions` - View all historical transactions.

### 3. Transactions (Protected - 2FA Required)
*   **Initiate Transfer**: `POST /api/v1/transactions/transfer` - Request a fund transfer. This sends a 6-digit code to your email.
*   **Authorize Transfer**: `POST /api/v1/transactions/authorize` - Enter the 6-digit code to complete the money movement.

### 4. Payees (Protected)
*   **Manage Payees**: `GET/POST/DELETE` endpoints to manage your banking contacts (Account, Zelle, or Address).

### 5. System
*   **Health Check**: `GET /health` - Verify server status.

## Security
*   All protected routes require an `Authorization: Bearer {token}` header.
*   The Postman collection automatically handles token storage upon a successful login.
