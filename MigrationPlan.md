# Migration Plan: Python Direct-SQL to Laravel API with Sanctum

This document outlines the steps to migrate the current AI Banking Python tool to a robust Laravel-based API platform with secure authentication.

## 1. Prerequisites
- PHP 8.1+
- Composer
- MySQL (MAMP/Localhost)
- Laravel CLI

## 2. Laravel Project Setup
1. **Initialize Project:**
   ```bash
   composer create-project laravel/laravel ai-banking-api
   ```
2. **Install Sanctum:**
   ```bash
   composer require laravel/sanctum
   php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
   ```
3. **Database Configuration:**
   Update `.env` to connect to the `banking_system` database.

## 3. Database Migration & Refactoring
### 3.1 Refactoring `customers` to `users`
In Laravel, the `User` model is the default for authentication. We will repurpose the `customers` table or link it to a `users` table.
- Add `password`, `remember_token`, and `email_verified_at` to `customers`.
- Implement `HasApiTokens` trait in the `User` (or `Customer`) model.

### 3.2 Eloquent Models
Create models for:
- `Customer` (mapped to `customers`)
- `Account` (mapped to `accounts`)
- `Transaction` (mapped to `transactions`)

Define relationships:
- `Customer` hasMany `Account`
- `Account` hasMany `Transaction`
- `Account` belongsTo `Customer`

## 4. API Development
### 4.1 Authentication (Sanctum)
- **POST `/api/login`**: Authenticate user and return a Sanctum token.
- **POST `/api/logout`**: Revoke the current token.

### 4.2 Banking Endpoints (Protected by `auth:sanctum`)
- **GET `/api/customer/summary`**: Returns customer info and accounts.
- **GET `/api/accounts/{id}/transactions`**: Returns transaction history for an account.
- **POST `/api/transfer`**: Execute a fund transfer (with validation and transactions).
- **GET `/api/analytics/{account_id}`**: Returns spending/income analytics.

## 5. Security Enhancements
- **Middleware**: Use `auth:sanctum` for all banking routes.
- **Validation**: Implement Laravel Form Requests for input validation.
- **Transactions**: Use DB Transactions for fund transfers to ensure atomicity.
- **Hashed Passwords**: Ensure all passwords in the DB are hashed using Bcrypt.

## 6. Tool Refactoring
The MCP tools will be updated to use the `requests` library to communicate with the Laravel API instead of using `mysql-connector`. This decouples the AI from the database and adds a security layer.
