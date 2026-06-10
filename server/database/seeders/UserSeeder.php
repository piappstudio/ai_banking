<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\User;
use Illuminate\Support\Facades\Hash;

class UserSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        // Create test users with passwords
        User::create([
            'first_name' => 'Rajesh',
            'last_name' => 'Kumar',
            'email' => 'rajesh@example.com',
            'phone' => '9876543210',
            'password' => Hash::make('SecurePass123'),
            'verified_email' => true,
            'email_verified_at' => now(),
        ]);

        User::create([
            'first_name' => 'Priya',
            'last_name' => 'Singh',
            'email' => 'priya@example.com',
            'phone' => '9876543211',
            'password' => Hash::make('SecurePass123'),
            'verified_email' => true,
            'email_verified_at' => now(),
        ]);

        User::create([
            'first_name' => 'Amit',
            'last_name' => 'Patel',
            'email' => 'amit@example.com',
            'phone' => '9876543212',
            'password' => Hash::make('SecurePass123'),
            'verified_email' => true,
            'email_verified_at' => now(),
        ]);
    }
}
