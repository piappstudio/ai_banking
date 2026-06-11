<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Payee extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id',
        'nickname',
        'account_number',
        'routing_number',
        'address',
        'phone_number',
        'email',
    ];

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
