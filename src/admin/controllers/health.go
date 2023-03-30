package controllers

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"pks.pyfreebilling.com/services"
)

// HealthCheck godoc
//
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
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":   true,
			"message": "Error executing health",
		})
		return
	}
	c.JSON(http.StatusOK, result)
}
