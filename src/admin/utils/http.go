package utils

import "pks.pyfreebilling.com/utils/filters"

// ResponseHTTP represents response body of this API for documentation purpose
type ResponseHTTP struct {
	Error   bool        `json:"error" example:"false"`
	Message string      `json:"message"`
	Data    interface{} `json:"data"`
}

// PaginatedResponseHTTP represents response body of this API for documentation purpose
type PaginatedResponseHTTP struct {
	Error      bool               `json:"error" example:"false"`
	Message    string             `json:"message"`
	Data       interface{}        `json:"data"`
	Pagination filters.Pagination `json:"pagination"`
}

// ResponseErrorHTTP represents response body of this API for documentation purpose
type ResponseErrorHTTP struct {
	Error   bool   `json:"error" example:"true"`
	Message string `json:"message"`
}
