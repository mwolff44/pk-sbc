package controllers

import (
	"fmt"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/go-playground/validator"
	"pks.pyfreebilling.com/models"
	"pks.pyfreebilling.com/services"
)

// GetGateways  godoc
// @Summary Get a paginated list of gateways
// @Description Responds with the list of gateways as JSON.
// @Tags gateways
// @Produce json
// @Success 200 {array} models.Gateway
// @Router /gateways [get]
func GetGateways(c *gin.Context) {
	pageStr := c.DefaultQuery("page", "1")
	const gatewaysPerPage = 5

	gateways, p, err := services.GatewaysService.ListGateways(pageStr, gatewaysPerPage)
	if err != nil {
		c.AbortWithStatus(http.StatusInternalServerError)
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"gateways": gateways,
		"p":        p,
	})
}

// CreateGateways  godoc
// @Summary Creates a new gateway object
// @Description Takes a gateway JSON and stores in DB. Return saved JSON.
// @Tags gateways
// @Produce json
// @Param gateway body models.Gateway true "gateway object"
// @Success 200 {object} models.Gateway
// @Router /gateways/ [post]
func CreateGateway(c *gin.Context) {
	var gateway models.Gateway
	if err := c.ShouldBind(&gateway); err != nil {
		verrs := err.(validator.ValidationErrors)
		messages := make([]string, len(verrs))
		for i, verr := range verrs {
			messages[i] = fmt.Sprintf(
				"%s is required, but was empty.",
				verr.Field())
		}
		c.JSON(http.StatusBadRequest,
			gin.H{"errors": messages})
		return
	}

	newGateway, saverr := services.GatewaysService.CreateGateway(gateway)
	if saverr != nil {
		log.Printf("error in flashes saving session: %s", saverr)
		c.AbortWithStatus(http.StatusInternalServerError)
		return
	}

	c.JSON(http.StatusOK, newGateway)
}

// GetGatewayByID  godoc
// @Summary Gets a gateway by ID
// @Description Returns the gateway whose id matches the id.
// @Tags gateways
// @Produce json
// @Param id path string true "search gateway by id"
// @Success 200 {object} models.Gateway
// @Router /gateways/{id} [get]
func GetGatewayByID(c *gin.Context) {
	id := c.Params.ByName("id")

	gateway, apiErr := services.GatewaysService.GetGateway(id)
	if apiErr != nil {
		c.JSON(apiErr.Status, apiErr)
		return
	}

	c.JSON(http.StatusOK, gateway)
}

// UpdateGateway update a gateway
func UpdateGateway(c *gin.Context) {
	var gateway models.Gateway
	id := c.Params.ByName("id")
	_, err := services.GatewaysService.GetGateway(id)
	if err != nil {
		c.JSON(http.StatusNotFound, gateway)
	}
	c.BindJSON(&gateway)
	updatedGateway, UpdateErr := services.GatewaysService.UpdateGateway(gateway)
	if UpdateErr != nil {
		c.AbortWithStatus(http.StatusNotFound)
	} else {
		c.JSON(http.StatusOK, updatedGateway)
	}
}

// DeleteGateway deletes from DB a gateway
func DeleteGateway(c *gin.Context) {
	id := c.Params.ByName("id")
	err := services.GatewaysService.DeleteGateway(id)
	if err != nil {
		c.AbortWithStatus(http.StatusNotFound)
	} else {
		c.JSON(http.StatusOK, gin.H{"id" + id: "is deleted"})
	}
}
