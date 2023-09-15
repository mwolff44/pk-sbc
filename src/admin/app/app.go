package app

import (
	"log"

	"github.com/Depado/ginprom"
	"github.com/gin-gonic/gin"
)

var (
	r *gin.Engine
)

func SetupRouter() *gin.Engine {
	// Set the router as the default one provided by Gin
	r = gin.Default()

	//r.Static("/static", "./static/")
	//r.LoadHTMLGlob("templates/*/*.html")

	p := ginprom.New(
		ginprom.Engine(r),
		ginprom.Namespace("pyfb"),
		ginprom.Subsystem("pks_admin"),
		ginprom.Path("/metrics"),
	)
	r.Use(p.Instrument())

	return r
}

// StartApp function starts the whole application
func StartApp() {

	// Initialize the routes
	mapUrls()

	// Start serving the application
	if err := r.Run(":3000"); err != nil {
		log.Fatalf("Failed to initialize server: %v\n", err)
		panic(err)
	}

}
