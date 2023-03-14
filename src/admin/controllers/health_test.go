package controllers

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
	"pks.pyfreebilling.com/services"
	"pks.pyfreebilling.com/utils/api_errors"
)

var (
	healthFunc func() (string, *api_errors.ApiError)
)

type healthServiceMock struct{}

func (*healthServiceMock) Health() (string, *api_errors.ApiError) {
	return healthFunc()
}

func TestHealthWithError(t *testing.T) {
	// init
	// Mock HealthService methods
	healthFunc = func() (string, *api_errors.ApiError) {
		return "", &api_errors.ApiError{Status: http.StatusInternalServerError, Message: "Error executing health"}
	}
	services.HealthService = &healthServiceMock{}

	response := httptest.NewRecorder()
	c, _ := gin.CreateTestContext(response)
	c.Request, _ = http.NewRequest(http.MethodGet, "", nil)

	HealthCheck(c)

	assert.EqualValues(t, http.StatusInternalServerError, response.Code)

	var apiErr api_errors.ApiError
	err := json.Unmarshal(response.Body.Bytes(), &apiErr)
	assert.Nil(t, err)

	assert.EqualValues(t, "Error executing health", apiErr.Message)
}

func TestHealthNoError(t *testing.T) {
	// init
	healthFunc = func() (string, *api_errors.ApiError) {
		return "Working fine !", nil
	}
	services.HealthService = &healthServiceMock{}

	response := httptest.NewRecorder()
	c, _ := gin.CreateTestContext(response)
	c.Request, _ = http.NewRequest(http.MethodGet, "", nil)

	HealthCheck(c)

	assert.EqualValues(t, http.StatusOK, response.Code)

	var body string
	err := json.Unmarshal(response.Body.Bytes(), &body)
	assert.Nil(t, err)

	assert.EqualValues(t, "Working fine !", body)
}
