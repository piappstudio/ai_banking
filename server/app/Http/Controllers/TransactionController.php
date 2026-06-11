<?php

namespace App\Http\Controllers;

use App\Models\Account;
use App\Models\Transaction;
use App\Models\TransactionVerification;
use App\Http\Resources\TransactionResource;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Mail;
use App\Mail\TransactionCodeMail;
use Illuminate\Validation\ValidationException;

class TransactionController extends BaseController
{
    /**
     * Step 1: Initiate transfer - generate and send 6-digit code.
     */
    public function transfer(Request $request)
    {
        $validated = $request->validate([
            'from_account_id' => 'required|exists:accounts,id',
            'to_account_id' => 'nullable|different:from_account_id',
            'to_payee_id' => 'nullable|exists:payees,id',
            'amount' => 'required|numeric|min:0.01',
            'description' => 'nullable|string|max:255',
        ]);

        $toAccountValue = $request->input('to_account_id');
        $toPayeeValue = $request->input('to_payee_id');

        if (($toAccountValue === null || $toAccountValue == 0) && $toPayeeValue === null) {
            return $this->errorResponse('Either to_account_id or to_payee_id is required', 422);
        }

        $fromAccount = $request->user()->accounts()->find($validated['from_account_id']);
        if (!$fromAccount) {
            return $this->errorResponse('Sender account not found or access denied', 403);
        }

        if ($fromAccount->balance < $validated['amount']) {
            return $this->errorResponse('Insufficient balance', 400);
        }

        $recipientName = 'External Transfer';
        $toAccount = null;
        $toPayee = null;

        if (!empty($validated['to_account_id']) && $validated['to_account_id'] != 0) {
            $toAccount = Account::find($validated['to_account_id']);
            $recipientName = $toAccount->account_number;
        } elseif (!empty($validated['to_payee_id'])) {
            $toPayee = \App\Models\Payee::find($validated['to_payee_id']);
            $recipientName = $toPayee->nickname;
        }

        // Generate 6-digit code
        $code = (string) random_int(100000, 999999);

        // Store verification request
        $verification = TransactionVerification::create([
            'user_id' => $request->user()->id,
            'from_account_id' => $fromAccount->id,
            'to_account_id' => $toAccount ? $toAccount->id : null,
            'to_payee_id' => $toPayee ? $toPayee->id : null,
            'amount' => $validated['amount'],
            'description' => $validated['description'] ?? 'Transfer to ' . $recipientName,
            'code' => $code,
            'expires_at' => now()->addMinutes(10),
        ]);

        // Send email with code
        try {
            Mail::to($request->user()->email)->send(new TransactionCodeMail(
                $code,
                $validated['amount'],
                $recipientName,
                $verification->description
            ));
        } catch (\Exception $e) {
            \Illuminate\Support\Facades\Log::error('Mail failed: ' . $e->getMessage());
        }

        return $this->successResponse([
            'verification_id' => $verification->id,
            'expires_at' => $verification->expires_at->toIso8601String(),
        ], 'Authorization code sent to your registered email.');
    }

    /**
     * Step 2: Complete transfer - verify code and perform transaction.
     */
    public function authorizeTransfer(Request $request)
    {
        $validated = $request->validate([
            'verification_id' => 'required|exists:transaction_verifications,id',
            'code' => 'required|string|size:6',
        ]);

        $verification = TransactionVerification::where('id', $validated['verification_id'])
            ->where('user_id', $request->user()->id)
            ->first();

        if (!$verification) {
            return $this->errorResponse('Invalid verification request', 404);
        }

        if ($verification->verified) {
            return $this->errorResponse('Transaction already completed', 400);
        }

        if ($verification->isExpired()) {
            return $this->errorResponse('Authorization code has expired', 400);
        }

        if ($verification->code !== $validated['code']) {
            return $this->errorResponse('Invalid authorization code', 400);
        }

        $fromAccount = Account::find($verification->from_account_id);

        if ($fromAccount->balance < $verification->amount) {
            return $this->errorResponse('Insufficient balance to complete the transaction', 400);
        }

        try {
            DB::beginTransaction();

            // Debit from sender
            $fromAccount->decrement('balance', $verification->amount);
            $debit = Transaction::create([
                'account_id' => $fromAccount->id,
                'transaction_type' => 'debit',
                'amount' => $verification->amount,
                'description' => $verification->description,
            ]);

            // If it's an internal transfer, credit the receiver
            if ($verification->to_account_id) {
                $toAccount = Account::find($verification->to_account_id);
                $toAccount->increment('balance', $verification->amount);
                Transaction::create([
                    'account_id' => $toAccount->id,
                    'transaction_type' => 'credit',
                    'amount' => $verification->amount,
                    'description' => $verification->description,
                ]);
            }

            // Mark as verified
            $verification->update(['verified' => true]);

            DB::commit();

            return $this->successResponse([
                'transaction' => new TransactionResource($debit)
            ], 'Transfer successful');
        } catch (\Exception $e) {
            DB::rollBack();
            return $this->errorResponse('Transfer failed: ' . $e->getMessage(), 500);
        }
    }
}
