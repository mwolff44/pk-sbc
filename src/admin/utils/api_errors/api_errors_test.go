package api_errors

import (
	"net/http"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestNewInternalServerError(t *testing.T) {
	err := NewInternalServerError("this is the message: database error")
	assert.NotNil(t, err)
	assert.EqualValues(t, http.StatusInternalServerError, err.Status)
	assert.EqualValues(t, "this is the message: database error", err.Message)
	assert.EqualValues(t, "internal_server_error", err.Error)
}

func TestNewBadRequestError(t *testing.T) {
	//TODO: Test!
}

func TestNewNotFoundError(t *testing.T) {
	//TODO: Test!
}
