package app

import (
	"pks.pyfreebilling.com/controllers"
)

// mapUrls function lists the project urls
func mapUrls() {

	// Handle the gateway's routes
	r.GET("/gateways/", controllers.GetGateways)
	r.POST("/gateways/", controllers.CreateGateway)
	r.GET("/gateways/:id", controllers.GetGatewayByID)
	r.PUT("/gateways/:id", controllers.UpdateGateway)
	r.DELETE("/gateways/:id", controllers.DeleteGateway)

	// Handle health route
	r.GET("/health", controllers.HealthCheck)

}
