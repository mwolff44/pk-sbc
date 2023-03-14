package app

import (
	"net/http"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestMappings(t *testing.T) {

	assert.EqualValues(t, 0, len(r.Routes()))

	mapUrls()

	routes := r.Routes()

	assert.EqualValues(t, 2, len(routes))

	assert.EqualValues(t, http.MethodGet, routes[0].Method)
	assert.EqualValues(t, "/gateways/", routes[0].Path)

	assert.EqualValues(t, http.MethodGet, routes[1].Method)
	assert.EqualValues(t, "/gateways/news", routes[1].Path)

	assert.EqualValues(t, http.MethodPost, routes[2].Method)
	assert.EqualValues(t, "/gateways/news", routes[2].Path)

	assert.EqualValues(t, http.MethodGet, routes[3].Method)
	assert.EqualValues(t, "/", routes[3].Path)

	assert.EqualValues(t, http.MethodGet, routes[4].Method)
	assert.EqualValues(t, "/health", routes[4].Path)
}
