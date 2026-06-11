<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class PayeeResource extends JsonResource
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
            'nickname' => $this->nickname,
            'accountNumber' => $this->account_number,
            'routingNumber' => $this->routing_number,
            'address' => $this->address,
            'phoneNumber' => $this->phone_number,
            'email' => $this->email,
            'createdAt' => $this->created_at->toIso8601String(),
        ];
    }
}
