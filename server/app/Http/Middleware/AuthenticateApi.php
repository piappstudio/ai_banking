<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Auth\AuthenticationException;

class AuthenticateApi
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure(\Illuminate\Http\Request): (\Illuminate\Http\Response|\Illuminate\Http\RedirectResponse)  $next
     * @return \Illuminate\Http\Response|\Illuminate\Http\RedirectResponse
     */
    public function handle(Request $request, Closure $next)
    {
        // Check if token is provided in Authorization header
        if (!$request->bearerToken()) {
            return response()->json([
                'success' => false,
                'message' => 'Unauthorized - Bearer token required',
                'errors' => ['Provide token in Authorization header: Bearer YOUR_TOKEN'],
            ], 401);
        }

        // Try to authenticate with Sanctum
        if (auth('sanctum')->check()) {
            return $next($request);
        }

        return response()->json([
            'success' => false,
            'message' => 'Unauthorized - Invalid or expired token',
            'errors' => ['Token is invalid or has expired'],
        ], 401);
    }
}
