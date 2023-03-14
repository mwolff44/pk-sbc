package services

import (
	"pks.pyfreebilling.com/models"
)

// GatewayService
var (
	GatewaysService gatewaysServiceInterface = &gatewaysService{}
)

type gatewaysService struct{}

type gatewaysServiceInterface interface {
	CreateGateway(models.Gateway) (*models.Gateway, error)
}

// SaveGateway function saves the gateway object and returns the saved object
func (s *gatewaysService) CreateGateway(gateway models.Gateway) (*models.Gateway, error) {
	if err := models.CreateGateway(&gateway); err != nil {
		return nil, err
	}

	return &gateway, nil
}
