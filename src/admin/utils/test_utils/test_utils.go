package testutils

import (
	"net/http"
	"net/http/httptest"

	"github.com/gin-gonic/gin"
)

// GetMockedContext mocks the request for test purpose
func GetMockedContext(request *http.Request, response *httptest.ResponseRecorder) *gin.Context {
	c, _ := gin.CreateTestContext(response)
	c.Request = request
	return c
}
