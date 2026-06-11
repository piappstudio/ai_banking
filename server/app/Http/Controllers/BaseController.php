<?php

namespace App\Http\Controllers;

use Illuminate\Http\JsonResponse;
use Illuminate\Http\Resources\Json\JsonResource;

class BaseController extends Controller
{
    /**
     * Success response with data.
     */
    protected function successResponse(
        mixed $data,
        string $message = 'Success',
        int $statusCode = 200,
    ): JsonResponse {
        $response = [
            'success' => true,
            'message' => $message,
        ];

        if ($data instanceof JsonResource) {
            $response['data'] = $data->resolve();
        } else {
            $response['data'] = $data;
        }

        return response()->json($response, $statusCode);
    }

    /**
     * Success response with paginated data.
     */
    protected function successPaginatedResponse(
        mixed $data,
        string $message = 'Success',
        int $statusCode = 200,
    ): JsonResponse {
        return response()->json([
            'success' => true,
            'message' => $message,
            'data' => $data->items(),
            'pagination' => [
                'total' => $data->total(),
                'count' => $data->count(),
                'perPage' => $data->perPage(),
                'currentPage' => $data->currentPage(),
                'lastPage' => $data->lastPage(),
                'hasMorePages' => $data->hasMorePages(),
            ],
        ], $statusCode);
    }

    /**
     * Error response.
     */
    protected function errorResponse(
        string $message,
        int $statusCode = 400,
        mixed $errors = null,
    ): JsonResponse {
        $response = [
            'success' => false,
            'message' => $message,
        ];

        if ($errors) {
            $response['errors'] = $errors;
        }

        return response()->json($response, $statusCode);
    }

    /**
     * Created response (201).
     */
    protected function createdResponse(
        mixed $data,
        string $message = 'Created successfully',
    ): JsonResponse {
        return $this->successResponse($data, $message, 201);
    }

    /**
     * No content response (204).
     */
    protected function noContentResponse(): JsonResponse
    {
        return response()->json(null, 204);
    }

    /**
     * Unauthorized response (401).
     */
    protected function unauthorizedResponse(string $message = 'Unauthorized'): JsonResponse
    {
        return $this->errorResponse($message, 401);
    }

    /**
     * Forbidden response (403).
     */
    protected function forbiddenResponse(string $message = 'Forbidden'): JsonResponse
    {
        return $this->errorResponse($message, 403);
    }

    /**
     * Not found response (404).
     */
    protected function notFoundResponse(string $message = 'Not found'): JsonResponse
    {
        return $this->errorResponse($message, 404);
    }

    /**
     * Validation error response (422).
     */
    protected function validationErrorResponse(array $errors): JsonResponse
    {
        return $this->errorResponse(
            'Validation failed',
            422,
            $errors,
        );
    }
}
