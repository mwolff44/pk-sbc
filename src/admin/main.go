package main

import (
	"log"

	"pks.pyfreebilling.com/app"
)

// @title           P-KISS-SBC API
// @version         1.0.0
// @description     This is the documentation API for P-KISS-SBC.
// @termsOfService  http://swagger.io/terms/

// @contact.name   Mathias WOLFF
// @contact.url    https://www.pyfreebilling.com

// @license.name  AGPL 3.0
// @license.url   http://www.apache.org/licenses/LICENSE-2.0.html

// @host      localhost:8080
// @BasePath  /api/v1

// @consumes application/json
// @produces application/json

// @securityDefinitions.basic  BasicAuth

// @externalDocs.description  OpenAPI
// @externalDocs.url          https://swagger.io/resources/open-api/
func main() {
	log.Println("Starting PKS-admin server...")

	app.StartApp()
}
