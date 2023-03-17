package app

import (
	swaggerFiles "github.com/swaggo/files"     // swagger embed files
	ginSwagger "github.com/swaggo/gin-swagger" // gin-swagger middleware
	"pks.pyfreebilling.com/controllers"
	_ "pks.pyfreebilling.com/docs"
)

// mapUrls function lists the project urls
func mapUrls() {

	api := r.Group("api/v1")
	{
		// Handle the gateway's routes
		api.GET("/gateways/", controllers.GetGateways)
		api.POST("/gateways/", controllers.CreateGateway)
		api.GET("/gateways/:id", controllers.GetGatewayByID)
		api.PUT("/gateways/:id", controllers.UpdateGateway)
		api.DELETE("/gateways/:id", controllers.DeleteGateway)
	}

	// Handle health route
	r.GET("/health", controllers.HealthCheck)

	//Register handler for Swagger
	r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))
}
