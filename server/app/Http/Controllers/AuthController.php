<?php

namespace App\Http\Controllers;

use App\Http\Requests\SignUpRequest;
use App\Http\Requests\LoginRequest;
use App\Http\Requests\VerifyEmailRequest;
use App\Http\Requests\ForgotPasswordRequest;
use App\Http\Requests\VerifyResetCodeRequest;
use App\Http\Requests\ResetPasswordRequest;
use App\Http\Requests\ResendVerificationCodeRequest;
use App\Http\Resources\UserResource;
use App\Models\User;
use App\Models\EmailVerification;
use App\Models\PasswordResetCode;
use Illuminate\Http\Request;
use Illuminate\Support\Str;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Mail;
use App\Mail\EmailVerificationMail;
use App\Mail\PasswordResetMail;
use Illuminate\Validation\ValidationException;
use Illuminate\Support\Facades\Log;

class AuthController extends BaseController
{
    /**
     * User signup - Create new user with email
     */
    public function signup(SignUpRequest $request)
    {
        try {
            // Create user with hashed password
            $user = new User([
                'first_name' => $request->validated('firstName'),
                'last_name' => $request->validated('lastName'),
                'email' => $request->validated('email'),
                'phone' => $request->validated('phone'),
                'password' => Hash::make($request->validated('password')),
            ]);
            $user->verified_email = false;
            $user->save();

            // Generate verification code
            $token = (string) random_int(100000, 999999);
            EmailVerification::create([
                'user_id' => $user->id,
                'token' => $token,
                'expires_at' => now()->addHours(24),
            ]);

            // Send verification email
            Mail::to($user->email)->send(new EmailVerificationMail($token));

            return $this->createdResponse(
                [
                    'user' => new UserResource($user),
                ],
                'User registered successfully. Please verify your email.',
            );
        } catch (\Exception $e) {
            Log::error('Registration error: ' . $e->getMessage(), ['exception' => $e]);
            return $this->errorResponse(
                'Registration failed. Please try again later.',
                500,
            );
        }
    }

    /**
     * Resend email verification code
     */
    public function resendVerificationCode(ResendVerificationCodeRequest $request)
    {
        try {
            $user = User::where('email', $request->validated('email'))->firstOrFail();

            if ($user->verified_email) {
                return $this->errorResponse('Email already verified.', 400);
            }

            // Delete existing tokens
            EmailVerification::where('user_id', $user->id)->delete();

            // Generate new verification code
            $token = (string) random_int(100000, 999999);
            EmailVerification::create([
                'user_id' => $user->id,
                'token' => $token,
                'expires_at' => now()->addHours(24),
            ]);

            // Send verification email
            Mail::to($user->email)->send(new EmailVerificationMail($token));

            return $this->successResponse(null, 'Verification code resent successfully.');
        } catch (\Exception $e) {
            Log::error('Resend verification code error: ' . $e->getMessage(), ['exception' => $e]);
            return $this->errorResponse('Failed to resend verification code. Please try again later.', 500);
        }
    }

    /**
     * Initiate password reset - send code
     */
    public function forgotPassword(ForgotPasswordRequest $request)
    {
        try {
            $email = $request->validated('email');

            // Delete any existing codes for this email
            PasswordResetCode::where('email', $email)->delete();

            // Generate 6-digit code
            $code = (string) random_int(100000, 999999);

            PasswordResetCode::create([
                'email' => $email,
                'code' => $code,
                'expires_at' => now()->addHour(),
            ]);

            // Send email
            Mail::to($email)->send(new PasswordResetMail($code));

            return $this->successResponse(null, 'If that email address exists in our system, we have sent a reset code.');
        } catch (\Exception $e) {
            Log::error('Forgot password error: ' . $e->getMessage(), ['exception' => $e]);
            return $this->errorResponse('Failed to send reset code. Please try again later.', 500);
        }
    }

    /**
     * Verify password reset code
     */
    public function verifyResetCode(VerifyResetCodeRequest $request)
    {
        try {
            $resetCode = PasswordResetCode::where('email', $request->validated('email'))
                ->where('code', $request->validated('code'))
                ->first();

            if (!$resetCode) {
                return $this->errorResponse('Invalid verification code.', 400);
            }

            if ($resetCode->isExpired()) {
                $resetCode->delete();
                return $this->errorResponse('Verification code has expired.', 400);
            }

            return $this->successResponse(null, 'Code verified successfully.');
        } catch (\Exception $e) {
            Log::error('Verify reset code error: ' . $e->getMessage(), ['exception' => $e]);
            return $this->errorResponse('Verification failed. Please try again later.', 500);
        }
    }

    /**
     * Reset password with code
     */
    public function resetPassword(ResetPasswordRequest $request)
    {
        try {
            $resetCode = PasswordResetCode::where('email', $request->validated('email'))
                ->where('code', $request->validated('code'))
                ->first();

            if (!$resetCode || $resetCode->isExpired()) {
                return $this->errorResponse('Invalid or expired verification code.', 400);
            }

            $user = User::where('email', $request->validated('email'))->firstOrFail();
            $user->password = Hash::make($request->validated('password'));
            $user->save();

            // Delete the code after use
            $resetCode->delete();

            return $this->successResponse(null, 'Password has been reset successfully. Please login with your new password.');
        } catch (\Exception $e) {
            Log::error('Reset password error: ' . $e->getMessage(), ['exception' => $e]);
            return $this->errorResponse('Password reset failed. Please try again later.', 500);
        }
    }

    /**
     * User login - Authenticate existing user
     */
    public function login(LoginRequest $request)
    {
        try {
            $user = User::where('email', $request->validated('email'))->firstOrFail();

            if (!Hash::check($request->validated('password'), $user->password)) {
                return $this->errorResponse('Invalid email or password', 401);
            }

            if (!$user->verified_email) {
                return $this->errorResponse('Please verify your email before logging in', 403);
            }

            $token = $user->createToken('auth_token')->plainTextToken;

            return $this->successResponse([
                'user' => new UserResource($user),
                'token' => $token,
                'tokenType' => 'Bearer',
            ], 'Login successful.');
        } catch (\Exception $e) {
            return $this->errorResponse('Login failed: Invalid email or password', 401);
        }
    }

    /**
     * Verify email with token
     */
    public function verifyEmail(VerifyEmailRequest $request)
    {
        try {
            $verification = EmailVerification::where('token', $request->validated('token'))
                ->whereHas('user', function ($query) use ($request) {
                    $query->where('email', $request->validated('email'));
                })
                ->first();

            if (!$verification) {
                return $this->errorResponse('Email verification failed: Invalid code or email', 400);
            }

            if ($verification->expires_at->isPast()) {
                $verification->delete();
                return $this->errorResponse('Email verification failed: Code has expired', 400);
            }

            $user = $verification->user;
            $user->verified_email = true;
            $user->email_verified_at = now();
            $user->save();

            $verification->delete();

            $token = $user->createToken('auth_token')->plainTextToken;

            return $this->successResponse([
                'user' => new UserResource($user),
                'token' => $token,
                'tokenType' => 'Bearer',
            ], 'Email verified successfully.');
        } catch (\Exception $e) {
            Log::error('Email verification error: ' . $e->getMessage(), ['exception' => $e]);
            return $this->errorResponse('Email verification failed. Please check your token or try again later.', 400);
        }
    }
}
