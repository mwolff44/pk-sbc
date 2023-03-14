package controllers

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"pks.pyfreebilling.com/services"
	"pks.pyfreebilling.com/utils/api_errors"
)

// HealthCheck function responds that the app is working
func HealthCheck(c *gin.Context) {
	result, err := services.HealthService.Health()
	if err != nil {
		apiErr := api_errors.NewInternalServerError("Error executing health")
		c.JSON(http.StatusInternalServerError, apiErr)
		return
	}
	c.JSON(http.StatusOK, result)
}
