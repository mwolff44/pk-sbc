package app

import (
	"pks.pyfreebilling.com/controllers"
)

// mapUrls function lists the project urls
func mapUrls() {

	// Handle GET requests

	// Handle defaut route
	r.GET("/", controllers.Home)

	// Handle the gateway's routes
	r.GET("/gateways/", controllers.GatewayIndex)
	r.GET("/gateways/new", controllers.GatewayNewGet)

	// Handle health route
	r.GET("/health", controllers.HealthCheck)

	// Handle POST requests

	// Handle the gateway's routes
	r.POST("/gateways/new", controllers.GatewayNewPost)
}
