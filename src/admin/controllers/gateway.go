package controllers

import (
	"log"
	"net/http"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"pks.pyfreebilling.com/models"
	"pks.pyfreebilling.com/services"
)

// GetGateways  godoc
// @Summary Get a paginated list of gateways
// @Description Responds with the list of gateways as JSON.
// @Tags gateways
// @Produce json
// @Success 200 {array} models.Gateway
// @Failure      400  {object}  api_errors.ApiError
// @Failure      404  {object}  api_errors.ApiError
// @Failure      500  {object}  api_errors.ApiError
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
	if err := c.ShouldBindJSON(&gateway); err != nil {
		c.JSON(http.StatusBadRequest,
			gin.H{"errors": err.Error()})
		return
	}
	gateway.CreatedAt = time.Now()

	newGateway, saverr := services.GatewaysService.CreateGateway(gateway)
	if saverr != nil {
		log.Printf("error in flashes saving session: %s", saverr)
		c.AbortWithStatus(http.StatusInternalServerError)
		return
	}

	c.Header("Location", c.FullPath()+"/"+strconv.Itoa(int(newGateway.ID)))

	c.JSON(http.StatusCreated, gin.H{"gateway": newGateway})
}

// GetGatewayByID  godoc
// @Summary Show a gateway
// @Description Get gateway by ID
// @Tags gateways
// @Produce json
// @Param id path string true "Gateway ID"
// @Success 200 {object} models.Gateway
// @Failure      400  {object}  api_errors.ApiError
// @Failure      404  {object}  api_errors.ApiError
// @Failure      500  {object}  api_errors.ApiError
// @Router /gateways/{id} [get]
func GetGatewayByID(c *gin.Context) {
	id := c.Params.ByName("id")

	gateway, apiErr := services.GatewaysService.GetGateway(id)
	if apiErr != nil {
		c.JSON(apiErr.Status, apiErr)
		return
	}

	c.Header("Last-Modified", gateway.UpdatedAt.String())

	c.JSON(http.StatusOK, gateway)
}

// UpdateGateway  godoc
// @Summary Update a gateway
// @Description update gateway.
// @Tags gateways
// @Produce json
// @Param id path string true "id of the gateway"
// @Success 200 {object} models.Gateway
// @Error 400 {string} "Invalid input"
// @Error 404 {string} "Invalid gateway ID"
// @Router /gateways/{id} [put]
// UpdateGateway update a gateway
func UpdateGateway(c *gin.Context) {
	var gateway models.Gateway
	id := c.Params.ByName("id")
	_, err := services.GatewaysService.GetGateway(id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{
			"error": "Gateway not found"})
		return
	}
	if err := c.ShouldBindJSON(&gateway); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": err.Error()})
		return
	}
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
