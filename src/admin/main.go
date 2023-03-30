package main

import (
	"log"

	"pks.pyfreebilling.com/app"
)

//	@title			P-KISS-SBC API
//	@version		1.0.0
//	@description	This is the documentation API for P-KISS-SBC.
//	@termsOfService	http://swagger.io/terms/

//	@contact.name	Mathias WOLFF
//	@contact.url	https://www.pyfreebilling.com

//	@license.name	AGPL 3.0
//	@license.url	https://www.gnu.org/licenses/agpl-3.0.en.html

//	@host		localhost:3000
//	@BasePath	/v1

//	@consumes	application/json
//	@produces	application/json

//	@securityDefinitions.basic	BasicAuth

// @externalDocs.description	OpenAPI
// @externalDocs.url			https://swagger.io/resources/open-api/
func main() {
	log.Println("Starting PKS-admin server...")

	app.StartApp()
}
