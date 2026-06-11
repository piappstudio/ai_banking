<?php

namespace App\Http\Controllers;

use App\Models\Payee;
use App\Http\Requests\AddPayeeRequest;
use App\Http\Resources\PayeeResource;
use Illuminate\Http\Request;

class PayeeController extends BaseController
{
    /**
     * List all payees for the authenticated user.
     */
    public function index(Request $request)
    {
        $payees = $request->user()->payees()->orderBy('nickname')->get();
        return $this->successResponse(PayeeResource::collection($payees));
    }

    /**
     * Add a new payee.
     */
    public function store(AddPayeeRequest $request)
    {
        $payee = Payee::create([
            'user_id' => $request->user()->id,
            'nickname' => $request->nickname,
            'account_number' => $request->accountNumber,
            'routing_number' => $request->routingNumber,
            'address' => $request->address,
            'phone_number' => $request->phoneNumber,
            'email' => $request->email,
        ]);

        return $this->createdResponse(
            new PayeeResource($payee),
            'Payee added successfully.'
        );
    }

    /**
     * Remove a payee.
     */
    public function destroy(Request $request, $id)
    {
        $payee = $request->user()->payees()->find($id);

        if (!$payee) {
            return $this->notFoundResponse('Payee not found');
        }

        $payee->delete();

        return $this->successResponse(null, 'Payee removed successfully');
    }
}
