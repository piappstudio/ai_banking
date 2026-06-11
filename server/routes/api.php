<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\AccountController;
use App\Http\Controllers\TransactionController;
use App\Http\Controllers\PayeeController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

Route::prefix('v1')->group(function () {
    // ============================================================================
    // Authentication Routes (Public - No Auth Required)
    // ============================================================================
    Route::prefix('auth')->group(function () {
        Route::post('/signup', [AuthController::class, 'signup']);
        Route::post('/login', [AuthController::class, 'login']);
        Route::post('/verify-email', [AuthController::class, 'verifyEmail']);
        Route::post('/resend-verification', [AuthController::class, 'resendVerificationCode']);
        Route::post('/forgot-password', [AuthController::class, 'forgotPassword']);
        Route::post('/verify-reset-code', [AuthController::class, 'verifyResetCode']);
        Route::post('/reset-password', [AuthController::class, 'resetPassword']);
    });

    // ============================================================================
    // Protected Routes (Require Authentication via Sanctum)
    // ============================================================================
    Route::middleware('auth:sanctum')->group(function () {
        // Account Routes
        Route::prefix('accounts')->group(function () {
            Route::get('/', [AccountController::class, 'index']);
            Route::get('/{id}', [AccountController::class, 'show']);
            Route::get('/{id}/transactions', [AccountController::class, 'transactions']);
        });

        // Transaction Routes
        Route::prefix('transactions')->group(function () {
            Route::post('/transfer', [TransactionController::class, 'transfer']);
            Route::post('/authorize', [TransactionController::class, 'authorizeTransfer']);
        });

        // Payee Routes
        Route::prefix('payees')->group(function () {
            Route::get('/', [PayeeController::class, 'index']);
            Route::post('/', [PayeeController::class, 'store']);
            Route::delete('/{id}', [PayeeController::class, 'destroy']);
        });
    });
});

// Health check endpoint (outside v1 prefix)
Route::get('/health', function () {
    return response()->json([
        'status' => 'ok',
        'message' => 'AI Banking API is running',
        'version' => '1.0.0',
    ]);
});
