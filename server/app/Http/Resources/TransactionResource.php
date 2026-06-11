<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class TransactionResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray($request)
    {
        return [
            'id' => $this->id,
            'accountId' => $this->account_id,
            'type' => $this->transaction_type,
            'amount' => (float) $this->amount,
            'description' => $this->description,
            'createdAt' => $this->created_at->toIso8601String(),
        ];
    }
}
