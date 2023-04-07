package controllers

import (
	"encoding/json"
	"errors"
	"io"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
	"pks.pyfreebilling.com/services"
	"pks.pyfreebilling.com/utils"
)

var (
	healthFunc func() (string, error)
)

type healthServiceMock struct{}

func (*healthServiceMock) Health() (string, error) {
	return healthFunc()
}

func TestHealthWithError(t *testing.T) {
	// init
	// Mock HealthService methods
	healthFunc = func() (string, error) {
		return "", errors.New("Error executing health")
	}
	services.HealthService = &healthServiceMock{}

	response := httptest.NewRecorder()
	c, _ := gin.CreateTestContext(response)
	c.Request, _ = http.NewRequest(http.MethodGet, "", nil)

	HealthCheck(c)

	assert.EqualValues(t, http.StatusInternalServerError, response.Code)

	var apiErr utils.ResponseErrorHTTP
	err := json.Unmarshal(response.Body.Bytes(), &apiErr)
	assert.Nil(t, err)

	assert.EqualValues(t, "Error executing health", apiErr.Message)
}

func TestHealthNoError(t *testing.T) {
	// init
	healthFunc = func() (string, error) {
		return "Working fine !", nil
	}
	services.HealthService = &healthServiceMock{}

	response := httptest.NewRecorder()
	c, _ := gin.CreateTestContext(response)
	c.Request, _ = http.NewRequest(http.MethodGet, "", nil)

	HealthCheck(c)

	assert.EqualValues(t, http.StatusOK, response.Code)

	body, _ := io.ReadAll(response.Body)

	assert.JSONEq(t, `{"data":null,"error":false,"message":"Working fine !"}`, string(body))
}
