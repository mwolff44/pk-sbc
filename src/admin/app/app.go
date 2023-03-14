package app

import (
	"embed"
	"html/template"
	"io/fs"
	"log"
	"net/http"
	"os"
	"path/filepath"

	"github.com/Depado/ginprom"
	"github.com/gin-contrib/sessions"
	"github.com/gin-contrib/sessions/cookie"
	"github.com/gin-gonic/gin"
	"pks.pyfreebilling.com/models"
)

var (
	r *gin.Engine
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

func setupRouter() *gin.Engine {
	// Set the router as the default one provided by Gin
	r = gin.Default()

	sessionKey := os.Getenv("PKS_SESSION_KEY")
	if sessionKey == "" {
		log.Fatal("error: set PKS_SESSION_KEY to a secret string and try again")
	}

	store := cookie.NewStore([]byte(sessionKey))
	r.Use(sessions.Sessions("mysession", store))

	tmpl := template.Must(template.ParseFS(tmplEmbed, "templates/*/*.html"))
	r.SetHTMLTemplate(tmpl)

	r.StaticFS("/static", http.FS(staticEmbed))

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

	// Initialize database
	models.SetupDatabase()

	// Define router info
	r := setupRouter()

	// Initialize the routes
	mapUrls()

	// Start serving the application
	if err := r.Run(":3000"); err != nil {
		log.Fatalf("Failed to initialize server: %v\n", err)
		panic(err)
	}

}
