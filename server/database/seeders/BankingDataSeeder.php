<?php

namespace Database\Seeders;

use App\Models\User;
use App\Models\Account;
use App\Models\Transaction;
use App\Models\Payee;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;
use Carbon\Carbon;
use Faker\Factory as Faker;

class BankingDataSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $faker = Faker::create();

        // Define date range
        $startDate = Carbon::create(2024, 1, 1);
        $endDate = Carbon::create(2026, 6, 1);

        // Descriptions for transactions
        $debitDescriptions = [
            'Grocery Store Purchase', 'Monthly Rent Payment', 'Electricity Bill', 'Water Bill',
            'Internet Subscription', 'Gym Membership', 'Restaurant Dinner', 'Gas Station',
            'Amazon Order', 'Netflix Subscription', 'Coffee Shop', 'Pharmacy',
            'Flight Booking', 'Hotel Stay', 'Uber Trip', 'Car Insurance',
            'Movie Theater', 'App Store Purchase', 'Department Store', 'Zelle Transfer Out'
        ];

        $creditDescriptions = [
            'Monthly Salary', 'Freelance Project Payment', 'Tax Refund', 'Dividend Payout',
            'Gift from Family', 'Zelle Transfer In', 'Venmo Cashout', 'Refund from Amazon',
            'Investment Interest', 'Bonus Payment'
        ];

        // 1. Create 20 Randomized Users
        for ($i = 0; $i < 20; $i++) {
            $user = User::create([
                'first_name' => $faker->firstName,
                'last_name' => $faker->lastName,
                'email' => $i === 0 ? 'demo@example.com' : $faker->unique()->safeEmail,
                'phone' => $faker->numerify('##########'),
                'password' => Hash::make('password'),
                'verified_email' => true,
                'email_verified_at' => $startDate->copy()->addDays(rand(1, 30)),
            ]);

            // 2. Each user gets 1 to 3 Accounts
            $numAccounts = rand(1, 3);
            for ($j = 0; $j < $numAccounts; $j++) {
                $account = Account::create([
                    'user_id' => $user->id,
                    'account_number' => $faker->unique()->numerify('##########'),
                    'balance' => 0, // Will calculate based on transactions
                    'created_at' => $startDate->copy()->addDays(rand(1, 60)),
                ]);

                // 3. Each account gets 50 to 100 Transactions spread from 2024 to 2026
                $numTransactions = rand(50, 100);
                $currentBalance = 0;

                for ($k = 0; $k < $numTransactions; $k++) {
                    $type = rand(0, 10) > 3 ? 'debit' : 'credit'; // More debits than credits
                    $amount = $type === 'debit' ? $faker->randomFloat(2, 5, 500) : $faker->randomFloat(2, 500, 3000);

                    if ($type === 'debit') {
                        $currentBalance -= $amount;
                        $description = $faker->randomElement($debitDescriptions);
                    } else {
                        $currentBalance += $amount;
                        $description = $faker->randomElement($creditDescriptions);
                    }

                    // Random date between 2024 and 2026
                    $randomDays = rand(0, $startDate->diffInDays($endDate));
                    $transactionDate = $startDate->copy()->addDays($randomDays);

                    Transaction::create([
                        'account_id' => $account->id,
                        'transaction_type' => $type,
                        'amount' => $amount,
                        'description' => $description,
                        'created_at' => $transactionDate,
                        'updated_at' => $transactionDate,
                    ]);
                }

                // Update account with final balance
                $account->update(['balance' => $currentBalance]);
            }

            // 4. Each user gets 3 to 5 Payees
            $numPayees = rand(3, 5);
            for ($l = 0; $l < $numPayees; $l++) {
                Payee::create([
                    'user_id' => $user->id,
                    'nickname' => $faker->words(2, true),
                    'account_number' => rand(0, 1) ? $faker->numerify('#########') : null,
                    'routing_number' => rand(0, 1) ? $faker->numerify('#########') : null,
                    'address' => rand(0, 1) ? $faker->address : null,
                    'phone_number' => rand(0, 1) ? $faker->phoneNumber : null,
                    'email' => rand(0, 1) ? $faker->safeEmail : null,
                ]);
            }
        }
    }
}
