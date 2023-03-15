package app

import (
	"net/http"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
)

func TestMappings(t *testing.T) {

	r = gin.Default()

	assert.EqualValues(t, 0, len(r.Routes()))

	mapUrls()

	routes := r.Routes()

	assert.EqualValues(t, 5, len(routes))

	assert.EqualValues(t, http.MethodGet, routes[0].Method)
	assert.EqualValues(t, "/", routes[0].Path)

	assert.EqualValues(t, http.MethodGet, routes[1].Method)
	assert.EqualValues(t, "/gateways/", routes[1].Path)

	assert.EqualValues(t, http.MethodGet, routes[2].Method)
	assert.EqualValues(t, "/gateways/new", routes[2].Path)

	assert.EqualValues(t, http.MethodGet, routes[3].Method)
	assert.EqualValues(t, "/health", routes[3].Path)

	assert.EqualValues(t, http.MethodPost, routes[4].Method)
	assert.EqualValues(t, "/gateways/new", routes[4].Path)

}
