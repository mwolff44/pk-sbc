package controllers

import (
	"errors"
	"fmt"
	"net/http"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
	"pks.pyfreebilling.com/models"
	"pks.pyfreebilling.com/services"
	"pks.pyfreebilling.com/utils/filters"
)

// GetGateways  godoc
//
//	@Summary		Get a paginated list of gateways
//	@Description	Responds with the list of gateways as JSON.
//	@Tags			gateways
//	@Produce		json
//	@Param			page		query		int		false	"int valid"		minimum(1)	maximum(10000000) default(1)
//	@Param			page_size	query		int		false	"int valid"		minimum(5)	maximum(100) default(5)
//	@Param			sort		query		string	false	"string enums"	Enums(id, name, ip_address, -id, -name, -ip_address) default(id)
//	@Success		200			{object}	utils.PaginatedResponseHTTP{data=models.Gateways}
//	@Error			400 {object} utils.ResponseErrorHTTP{}
//	@Error			404 {object} utils.ResponseErrorHTTP{}
//	@Failure		500	{object}	utils.ResponseErrorHTTP{}
//	@Router			/gateways [get]
func GetGateways(c *gin.Context) {
	var filter filters.Filters
	if err := c.ShouldBindQuery(&filter); err != nil {
		fmt.Printf("Invalid inputs : %v", err.Error())
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   true,
			"message": "Invalid inputs. Please check your inputs",
		})
		return
	}
	fmt.Printf("Filters OK : %v", filter)
	filter.Sort = filter.GetSort()
	filter.SortSafelist = []string{"id", "name", "ip_address", "-id", "-name", "-ip_address"}
	fmt.Printf("Filters OK : %v", filter)

	gateways, p, err := services.GatewaysService.ListGateways(filter)
	if err != nil {
		if err.Error() == "invalid page number" {
			c.JSON(http.StatusBadRequest, gin.H{
				"error":   true,
				"message": "Pagination error : invalid page number",
			})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":   true,
			"message": "Error in getting gateway list",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"error":      false,
		"message":    "Gateway list",
		"data":       gateways,
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
//	@Success		200		{object}	utils.ResponseHTTP{data=models.Gateway}
//	@Error			400 {object} utils.ResponseErrorHTTP{}
//	@Failure		500	{object}	utils.ResponseErrorHTTP{}
//	@Router			/gateways/ [post]
func CreateGateway(c *gin.Context) {
	var gateway models.Gateway
	if err := c.ShouldBindJSON(&gateway); err != nil {
		fmt.Printf("invalid json body: %s", err)
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   true,
			"message": "Invalid json body. Please check your inputs",
		})
		return
	}
	gateway.CreatedAt = time.Now()

	newGateway, saverr := services.GatewaysService.CreateGateway(gateway)
	if saverr != nil {
		fmt.Printf("error in creating gateway: %s", saverr)
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":   true,
			"message": "Error in creating gateway",
		})
		return
	}

	c.Header("Location", c.FullPath()+"/"+strconv.Itoa(int(newGateway.ID)))

	c.JSON(http.StatusCreated, gin.H{
		"error":   false,
		"message": "Gateway created",
		"data":    newGateway,
	})
}

// GetGatewayByID  godoc
//
//	@Summary		Show a gateway
//	@Description	Get gateway by ID
//	@Tags			gateways
//	@Produce		json
//	@Param			id	path		int	true	"Gateway ID"
//	@Success		200	{object}	utils.ResponseHTTP{data=models.Gateway}
//	@Error			400 {object} utils.ResponseErrorHTTP{}
//	@Error			404 {object} utils.ResponseErrorHTTP{}
//	@Failure		500	{object}	utils.ResponseErrorHTTP{}
//
//	@Header			200	{string}	Location	"/gateway/1"
//	@Router			/gateways/{id} [get]
func GetGatewayByID(c *gin.Context) {
	var req models.GetGatewayRequest
	if err := c.ShouldBindUri(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   true,
			"message": "Invalid input. Please check your inputs",
		})
		return
	}

	gateway, apiErr := services.GatewaysService.GetGateway(req.ID)
	if apiErr != nil {
		rStatus := http.StatusInternalServerError
		if errors.Is(apiErr, gorm.ErrRecordNotFound) {
			rStatus = http.StatusBadRequest
			apiErr = errors.New("id does not exists in database")
		}
		c.JSON(rStatus, gin.H{
			"error":   true,
			"message": apiErr.Error(),
		})
		return
	}

	c.Header("Last-Modified", gateway.UpdatedAt.String())

	c.JSON(http.StatusOK, gin.H{
		"error":   false,
		"message": "Requested gateway",
		"data":    gateway,
	})
}

// UpdateGateway  godoc
//
//	@Summary		Update a gateway
//	@Description	update gateway.
//	@Tags			gateways
//	@Produce		json
//	@Param			id	path		int	true	"id of the gateway"
//	@Success		200	{object}	utils.ResponseHTTP{data=models.Gateway}
//	@Error			400 {object} utils.ResponseErrorHTTP{}
//	@Error			404 {object} utils.ResponseErrorHTTP{}
//	@Router			/gateways/{id} [put]
//
// UpdateGateway update a gateway
func UpdateGateway(c *gin.Context) {
	var gateway models.Gateway

	var req models.GetGatewayRequest
	if err := c.ShouldBindUri(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   true,
			"message": "Invalid input. Please check your inputs",
		})
		return
	}

	if err := c.ShouldBindJSON(&gateway); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   true,
			"message": "Invalid json body. Please check your inputs",
		})
		return
	}

	_, dberr := services.GatewaysService.GetGateway(req.ID)
	if dberr != nil {
		c.JSON(http.StatusNotFound, gin.H{
			"error":   true,
			"message": "Gateway not found",
		})
		return
	}

	updatedGateway, UpdateErr := services.GatewaysService.UpdateGateway(gateway)
	if UpdateErr != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":   true,
			"message": "Error in updating gateway",
		})
	} else {
		c.JSON(http.StatusOK, gin.H{
			"error":   false,
			"message": "Gateway updated",
			"data":    updatedGateway,
		})
	}
}

// DeleteGateway  godoc
//
//	@Summary		Delete a gateway
//	@Description	delete gateway.
//	@Tags			gateways
//	@Produce		json
//	@Param			id	path		int	true	"id of the gateway"
//	@Success		200	{object}	utils.ResponseHTTP{}
//	@Error			400 {object} utils.ResponseErrorHTTP{}
//	@Error			404 {object} utils.ResponseErrorHTTP{}
//	@Router			/gateways/{id} [delete]
func DeleteGateway(c *gin.Context) {
	var req models.GetGatewayRequest
	if err := c.ShouldBindUri(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   true,
			"message": "Invalid input. Please check your inputs",
		})
		return
	}

	dbErr := services.GatewaysService.DeleteGateway(req.ID)
	if dbErr != nil {
		rStatus := http.StatusInternalServerError
		if errors.Is(dbErr, gorm.ErrRecordNotFound) {
			rStatus = http.StatusBadRequest
			dbErr = errors.New("id does not exists in database")
		}
		c.JSON(rStatus, gin.H{
			"error":   true,
			"message": dbErr.Error(),
		})
	} else {
		c.JSON(http.StatusOK, gin.H{
			"error":   false,
			"message": "Gateway successfully deleted",
			"data":    nil,
		})
	}
}
