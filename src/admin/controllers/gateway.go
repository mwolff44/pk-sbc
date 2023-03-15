package controllers

import (
	"fmt"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/go-playground/validator"
	"pks.pyfreebilling.com/flashmessage"
	"pks.pyfreebilling.com/models"
	"pks.pyfreebilling.com/services"
)

func GatewayIndex(c *gin.Context) {
	pageStr := c.DefaultQuery("page", "1")
	const gatewaysPerPage = 5

	gateways, p, err := services.GatewaysService.ListGateways(pageStr, gatewaysPerPage)
	if err != nil {
		c.AbortWithStatus(http.StatusInternalServerError)
		return
	}

	c.HTML(http.StatusOK, "gateways/index.html", gin.H{
		"gateways": gateways,
		"messages": flashmessage.Flashes(c),
		"p":        p,
	})
}

func GatewayNewGet(c *gin.Context) {
	c.HTML(http.StatusOK, "gateways/new.html", gin.H{
		"messages": flashmessage.Flashes(c),
	})
}

// GatewayNewPost saves after validation a new gateway object
func GatewayNewPost(c *gin.Context) {
	var gateway models.Gateway
	if err := c.ShouldBind(&gateway); err != nil {
		verrs := err.(validator.ValidationErrors)
		messages := make([]string, len(verrs))
		for i, verr := range verrs {
			messages[i] = fmt.Sprintf(
				"%s is required, but was empty.",
				verr.Field())
		}
		c.HTML(http.StatusBadRequest, "gateways/new.html",
			gin.H{"errors": messages})
		return
	}

	newGateway, saverr := services.GatewaysService.CreateGateway(gateway)
	if saverr != nil {
		log.Printf("error in flashes saving session: %s", saverr)
		c.AbortWithStatus(http.StatusInternalServerError)
		return
	}
	flashmessage.FlashMessage(c, fmt.Sprintf("New gateway '%s' saved successfully.", newGateway.Name))

	c.Redirect(http.StatusFound, "/gateways/")
}
