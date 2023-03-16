package controllers

import (
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
)

var (
	gatewayFunc func() (string, *error)
)

type gatewayServiceMock struct{}

func (*gatewayServiceMock) Health() (string, *error) {
	return gatewayFunc()
}

func TestGatewayIndex(t *testing.T) {

	response := httptest.NewRecorder()
	c, _ := gin.CreateTestContext(response)
	os.Setenv("PKS_SESSION_KEY", "dummy")
	//setupRouter(r, freshDb(t))

	c.Request, _ = http.NewRequest(http.MethodGet, "/", nil)

	//Home(c)

	assert.EqualValues(t, http.StatusOK, response.Code)

	body := response.Body.String()
	expected := "Hello, gin!"
	assert.EqualValues(t, expected, strings.Trim(body, " \r\n"))

}
