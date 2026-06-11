<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class AccountResource extends JsonResource
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
            'accountNumber' => $this->account_number,
            'balance' => (float) $this->balance,
            'createdAt' => $this->created_at->toIso8601String(),
        ];
    }
}
