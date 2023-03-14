package flashmessage

import (
	"log"

	"github.com/gin-contrib/sessions"
	"github.com/gin-gonic/gin"
)

func FlashMessage(c *gin.Context, message string) {
	session := sessions.Default(c)
	session.AddFlash(message)
	if err := session.Save(); err != nil {
		log.Printf("error in flashMessage saving session: %s", err)
	}
}

func Flashes(c *gin.Context) []interface{} {
	session := sessions.Default(c)
	flashes := session.Flashes()
	if len(flashes) != 0 {
		if err := session.Save(); err != nil {
			log.Printf("error in flashes saving session: %s", err)
		}
	}
	return flashes
}
