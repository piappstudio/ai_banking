<?php

namespace App\Http\Controllers;

use App\Models\Account;
use App\Models\Transaction;
use App\Http\Resources\TransactionResource;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Validation\ValidationException;

class TransactionController extends BaseController
{
    /**
     * Transfer funds between accounts.
     */
    public function transfer(Request $request)
    {
        $validated = $request->validate([
            'from_account_id' => 'required|exists:accounts,id',
            'to_account_id' => 'required|exists:accounts,id|different:from_account_id',
            'amount' => 'required|numeric|min:0.01',
            'description' => 'nullable|string|max:255',
        ]);

        $fromAccount = $request->user()->accounts()->find($validated['from_account_id']);
        if (!$fromAccount) {
            return $this->errorResponse('Sender account not found or access denied', 403);
        }

        if ($fromAccount->balance < $validated['amount']) {
            return $this->errorResponse('Insufficient balance', 400);
        }

        $toAccount = Account::find($validated['to_account_id']);

        try {
            DB::beginTransaction();

            // Debit from sender
            $fromAccount->decrement('balance', $validated['amount']);
            Transaction::create([
                'account_id' => $fromAccount->id,
                'transaction_type' => 'debit',
                'amount' => $validated['amount'],
                'description' => $validated['description'] ?? 'Transfer to ' . $toAccount->account_number,
            ]);

            // Credit to receiver
            $toAccount->increment('balance', $validated['amount']);
            Transaction::create([
                'account_id' => $toAccount->id,
                'transaction_type' => 'credit',
                'amount' => $validated['amount'],
                'description' => $validated['description'] ?? 'Transfer from ' . $fromAccount->account_number,
            ]);

            DB::commit();

            return $this->successResponse(null, 'Transfer successful');
        } catch (\Exception $e) {
            DB::rollBack();
            return $this->errorResponse('Transfer failed: ' . $e->getMessage(), 500);
        }
    }
}
