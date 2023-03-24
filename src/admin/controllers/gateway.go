package controllers

import (
	"log"
	"net/http"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"pks.pyfreebilling.com/models"
	"pks.pyfreebilling.com/services"
	"pks.pyfreebilling.com/utils/api_errors"
	"pks.pyfreebilling.com/utils/filters"
)

// GetGateways  godoc
//
//	@Summary		Get a paginated list of gateways
//	@Description	Responds with the list of gateways as JSON.
//	@Tags			gateways
//	@Produce		json
//	@Param			page		query		int		false	"int valid"		minimum(1)	maximum(10_000_000)
//	@Param			page_size	query		int		false	"int valid"		minimum(5)	maximum(100)
//	@Param			sort		query		string	false	"string enums"	Enums(id, name, ip_address, -id, -name, -ip_address)
//	@Success		200			{array}		models.Gateways
//	@Failure		400			{object}	api_errors.ApiError
//	@Failure		404			{object}	api_errors.ApiError
//	@Failure		500			{object}	api_errors.ApiError
//	@Router			/gateways [get]
func GetGateways(c *gin.Context) {
	var filter filters.Filters
	if err := c.ShouldBindQuery(&filter); err != nil {
		log.Printf("Invalid inputs : %v", err.Error())
		apiErr := api_errors.NewBadRequestError("Invalid inputs. Please check your inputs")
		c.JSON(apiErr.Status, apiErr)
		return
	}
	filter.Sort = filter.GetSort()
	filter.SortSafelist = []string{"id", "name", "ip_address", "-id", "-name", "-ip_address"}
	log.Printf("Filters OK : %v", filter)

	gateways, p, err := services.GatewaysService.ListGateways(filter)
	if err != nil {
		if err.Error() == "invalid page number" {
			apiErr := api_errors.NewBadRequestError("Pagination error : invalid page number")
			c.JSON(apiErr.Status, apiErr)
			return
		}
		c.AbortWithStatus(http.StatusInternalServerError)
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"gateways":   gateways,
		"pagination": p,
	})
}

// CreateGateways  godoc
//
//	@Summary		Creates a new gateway object
//	@Description	Takes a gateway JSON and stores in DB. Return saved JSON.
//	@Tags			gateways
//	@Produce		json
//	@Param			gateway	body		models.Gateway	true	"gateway object"
//	@Success		200		{object}	models.Gateway
//	@Router			/gateways/ [post]
func CreateGateway(c *gin.Context) {
	var gateway models.Gateway
	if err := c.ShouldBindJSON(&gateway); err != nil {
		log.Printf("invalid json body: %s", err)
		apiErr := api_errors.NewBadRequestError("invalid json body")
		c.JSON(http.StatusBadRequest, apiErr)
		return
	}
	gateway.CreatedAt = time.Now()

	newGateway, saverr := services.GatewaysService.CreateGateway(gateway)
	if saverr != nil {
		log.Printf("error in creating gateway: %s", saverr)
		c.AbortWithStatus(http.StatusInternalServerError)
		return
	}

	c.Header("Location", c.FullPath()+"/"+strconv.Itoa(int(newGateway.ID)))

	c.JSON(http.StatusCreated, gin.H{"gateway": newGateway})
}

// GetGatewayByID  godoc
//
//	@Summary		Show a gateway
//	@Description	Get gateway by ID
//	@Tags			gateways
//	@Produce		json
//	@Param			id	path		string	true	"Gateway ID"
//	@Success		200	{object}	models.Gateway
//	@Failure		400	{object}	api_errors.ApiError
//	@Failure		404	{object}	api_errors.ApiError
//	@Failure		500	{object}	api_errors.ApiError
//
//	@Header			200	{string}	Location	"/gateway/1"
//	@Router			/gateways/{id} [get]
func GetGatewayByID(c *gin.Context) {
	var req models.GetGatewayRequest
	if err := c.ShouldBindUri(&req); err != nil {
		apiErr := api_errors.NewBadRequestError(err.Error())
		c.JSON(apiErr.Status, apiErr)
		return
	}

	gateway, apiErr := services.GatewaysService.GetGateway(req.ID)
	if apiErr != nil {
		c.JSON(apiErr.Status, apiErr)
		return
	}

	c.Header("Last-Modified", gateway.UpdatedAt.String())

	c.JSON(http.StatusOK, gateway)
}

// UpdateGateway  godoc
//
//	@Summary		Update a gateway
//	@Description	update gateway.
//	@Tags			gateways
//	@Produce		json
//	@Param			id	path		string	true	"id of the gateway"
//	@Success		200	{object}	models.Gateway
//	@Error			400 {string} "Invalid input"
//	@Error			404 {string} "Invalid gateway ID"
//	@Router			/gateways/{id} [put]
//
// UpdateGateway update a gateway
func UpdateGateway(c *gin.Context) {
	var gateway models.Gateway

	id, err := strconv.ParseInt(c.Params.ByName("id"), 10, 64)
	if err != nil {
		apiErr := api_errors.NewBadRequestError("Gateway ID must be an int64")
		c.JSON(http.StatusBadRequest, apiErr)
		return
	}
	if id <= 0 {
		apiErr := api_errors.NewBadRequestError("Gateway ID must be a number > 0")
		c.JSON(http.StatusBadRequest, apiErr)
		return
	}

	_, dberr := services.GatewaysService.GetGateway(id)
	if dberr != nil {
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
	id, err := strconv.ParseInt(c.Params.ByName("id"), 10, 64)
	if err != nil {
		apiErr := api_errors.NewBadRequestError("Gateway ID must be an int64")
		c.JSON(http.StatusBadRequest, apiErr)
		return
	}
	if id <= 0 {
		apiErr := api_errors.NewBadRequestError("Gateway ID must be a number > 0")
		c.JSON(http.StatusBadRequest, apiErr)
		return
	}

	dberr := services.GatewaysService.DeleteGateway(id)
	if dberr != nil {
		c.AbortWithStatus(http.StatusNotFound)
	} else {
		c.JSON(http.StatusOK, gin.H{"message": "gateway successfully deleted"})
	}
}
