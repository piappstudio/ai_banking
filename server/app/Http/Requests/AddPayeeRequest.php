<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class AddPayeeRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return true;
    }

    /**
     * Get the validation rules that apply to the request.
     */
    public function rules(): array
    {
        return [
            'nickname' => ['required', 'string', 'max:100'],
            'accountNumber' => ['nullable', 'string', 'max:50'],
            'routingNumber' => ['nullable', 'string', 'max:20'],
            'address' => ['nullable', 'string', 'max:255'],
            'phoneNumber' => ['nullable', 'string', 'max:20'],
            'email' => ['nullable', 'email', 'max:255'],
        ];
    }

    /**
     * Configure the validator instance.
     */
    public function withValidator($validator)
    {
        $validator->after(function ($validator) {
            $data = $validator->getData();
            $hasIdentifier = !empty($data['accountNumber']) ||
                             !empty($data['phoneNumber']) ||
                             !empty($data['email']);

            if (!$hasIdentifier) {
                $validator->errors()->add('identifier', 'At least one identifier (Account Number, Phone Number, or Email) must be provided.');
            }
        });
    }
}
