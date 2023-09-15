package main

import (
	"embed"
	"html/template"
	"io/fs"
	"log"
	"net/http"
	"path/filepath"

	"pks.pyfreebilling.com/app"
	"pks.pyfreebilling.com/models"
)

//go:embed templates
var tmplEmbed embed.FS

//go:embed static
var staticEmbedFS embed.FS

type staticFS struct {
	fs fs.FS
}

func (sfs *staticFS) Open(name string) (fs.File, error) {
	return sfs.fs.Open(filepath.Join("static", name))
}

var staticEmbed = &staticFS{staticEmbedFS}

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

	dbTarget := "pyfb.db"

	tmpl := template.Must(template.ParseFS(tmplEmbed, "templates/*/*.html"))

	// Initialize database
	models.SetupDatabase(dbTarget)

	// Define router info
	r := app.SetupRouter()
	r.SetHTMLTemplate(tmpl)
	r.StaticFS("/static", http.FS(staticEmbed))

	app.StartApp()
}
