package api_errors

import "net/http"

// ApiError structure
type ApiError struct {
	Status  int    `json:"status"`
	Message string `json:"message"`
	Error   string `json:"error,omitempty"`
}

// NewBadRequestError sends the approriate error message
func NewBadRequestError(message string) *ApiError {
	return &ApiError{
		Message: message,
		Status:  http.StatusBadRequest,
		Error:   "bad_request",
	}
}

// NewNotFoundError sends the approriate error message
func NewNotFoundError(message string) *ApiError {
	return &ApiError{
		Message: message,
		Status:  http.StatusNotFound,
		Error:   "not_found",
	}
}

// NewInternalServerError sends the approriate error message
func NewInternalServerError(message string) *ApiError {
	return &ApiError{
		Message: message,
		Status:  http.StatusInternalServerError,
		Error:   "internal_server_error",
	}
}
