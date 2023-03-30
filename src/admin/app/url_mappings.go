package app

import (
	swaggerFiles "github.com/swaggo/files"     // swagger embed files
	ginSwagger "github.com/swaggo/gin-swagger" // gin-swagger middleware
	"pks.pyfreebilling.com/controllers"
	_ "pks.pyfreebilling.com/docs"
)

// mapUrls function lists the project urls
func mapUrls() {

	api := r.Group("v1")

	// Handle the gateway's routes
	gr := api.Group("gateways")
	{
		gr.GET("", controllers.GetGateways)
		gr.POST("", controllers.CreateGateway)
		gr.GET("/:id", controllers.GetGatewayByID)
		gr.PUT("/:id", controllers.UpdateGateway)
		gr.DELETE("/:id", controllers.DeleteGateway)
	}

	// Handle health route
	api.GET("/health", controllers.HealthCheck)

	//Register handler for Swagger
	r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))
}
