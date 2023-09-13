package app

import (
	"net/http"

	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"     // swagger embed files
	ginSwagger "github.com/swaggo/gin-swagger" // gin-swagger middleware
	"pks.pyfreebilling.com/controllers"
	_ "pks.pyfreebilling.com/docs"
)

// mapUrls function lists the project urls
func mapUrls() {

	r.GET("/", func(c *gin.Context) {
		c.HTML(
			http.StatusOK,
			"index.html",
			gin.H{
				"title": "Home Page",
			},
		)
	})

	gw := r.Group("gateways")
	gw.GET("", controllers.GetGateways)
	gw.GET("/new", controllers.CreateGatewayGet)
	gw.POST("/new", controllers.CreateGateway)
	gw.GET("/:id", controllers.GetGatewayByID)
	gw.DELETE("/:id", controllers.DeleteGateway)

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
