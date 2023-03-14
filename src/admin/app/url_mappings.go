package app

import (
	"pks.pyfreebilling.com/controllers"
)

// mapUrls function lists the project urls
func mapUrls() {

	// Handle the GET requests at /balance/some_customer_id
	// Handle the balance status route

	r.GET("/gateways/", controllers.GatewayIndex)
	r.GET("/gateways/new", controllers.GatewayNewGet)
	r.POST("/gateways/new", controllers.GatewayNewPost)
	r.GET("/", controllers.Home)

	// Handle the GET requests at /health
	// Handle the health check route
	r.GET("/health", controllers.HealthCheck)
}
