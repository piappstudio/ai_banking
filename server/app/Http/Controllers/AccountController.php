<?php

namespace App\Http\Controllers;

use App\Models\Account;
use App\Http\Resources\AccountResource;
use Illuminate\Http\Request;

class AccountController extends BaseController
{
    /**
     * Display a listing of the accounts for the authenticated user.
     */
    public function index(Request $request)
    {
        $accounts = $request->user()->accounts;
        return $this->successResponse(AccountResource::collection($accounts));
    }

    /**
     * Display the specified account.
     */
    public function show(Request $request, $id)
    {
        $account = $request->user()->accounts()->find($id);

        if (!$account) {
            return $this->notFoundResponse('Account not found');
        }

        return $this->successResponse(new AccountResource($account));
    }

    /**
     * Get transactions for a specific account.
     */
    public function transactions(Request $request, $id)
    {
        $account = $request->user()->accounts()->find($id);

        if (!$account) {
            return $this->notFoundResponse('Account not found');
        }

        $transactions = $account->transactions()->orderBy('created_at', 'desc')->get();
        return $this->successResponse(\App\Http\Resources\TransactionResource::collection($transactions));
    }
}
