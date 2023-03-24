package controllers

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"pks.pyfreebilling.com/services"
	"pks.pyfreebilling.com/utils/api_errors"
)

// HealthCheck godoc
//	@Summary		Show the status of server.
//	@Description	get the status of server.
//	@Tags			root
//	@Accept			*/*
//	@Produce		json
//	@Success		200	{object}	map[string]interface{}
//	@Router			/health [get]
func HealthCheck(c *gin.Context) {
	result, err := services.HealthService.Health()
	if err != nil {
		apiErr := api_errors.NewInternalServerError("Error executing health")
		c.JSON(http.StatusInternalServerError, apiErr)
		return
	}
	c.JSON(http.StatusOK, result)
}
