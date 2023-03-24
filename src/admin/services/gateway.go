package services

import (
	"errors"
	"log"

	"gorm.io/gorm"
	"pks.pyfreebilling.com/models"
	"pks.pyfreebilling.com/utils/api_errors"
	"pks.pyfreebilling.com/utils/filters"
)

// GatewayService
var (
	GatewaysService gatewaysServiceInterface = &gatewaysService{}
)

type gatewaysService struct{}

type gatewaysServiceInterface interface {
	GetGateway(id int64) (*models.Gateway, *api_errors.ApiError)
	CreateGateway(models.Gateway) (*models.Gateway, error)
	UpdateGateway(models.Gateway) (*models.Gateway, error)
	DeleteGateway(id int64) error
	ListGateways(filter filters.Filters) (*models.Gateways, *filters.Pagination, error)
}

// GetGateway gets the gateway object by id
func (s *gatewaysService) GetGateway(id int64) (*models.Gateway, *api_errors.ApiError) {
	var gateway models.Gateway
	if err := models.GetGateway(&gateway, id); err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, api_errors.NewNotFoundError("Id does not exists in DB")
		}
		return nil, api_errors.NewInternalServerError("error when tying to get gateway : database error")
	}

	return &gateway, nil
}

// SaveGateway saves the gateway object and returns the saved object
func (s *gatewaysService) CreateGateway(gateway models.Gateway) (*models.Gateway, error) {
	if err := models.CreateGateway(&gateway); err != nil {
		return nil, err
	}

	return &gateway, nil
}

// UpdateGateway updates the gateway object and returns the updated object
func (s *gatewaysService) UpdateGateway(gateway models.Gateway) (*models.Gateway, error) {
	if err := models.UpdateGateway(&gateway); err != nil {
		return nil, err
	}

	return &gateway, nil
}

// DeleteGateway deletes the gateway object
func (s *gatewaysService) DeleteGateway(id int64) error {
	if err := models.DeleteGateway(id); err != nil {
		return err
	}

	return nil
}

// ListGateways returns a paginated list of gateways
func (s *gatewaysService) ListGateways(filter filters.Filters) (*models.Gateways, *filters.Pagination, error) {
	// Count total og gatesways in DB
	gatewayCount, err := models.CountGateways()
	if err != nil {
		return nil, nil, err
	}

	// Get pagination informations
	p, paginateErr := filters.Paginate(filter.Page, int(gatewayCount), filter.PageSize)
	if paginateErr != nil {
		// c.AbortWithStatus(http.StatusBadRequest)
		log.Printf("Pagination error : %s", paginateErr)
		return nil, nil, paginateErr
	}

	// Get gateways list
	var gateways models.Gateways
	if err := models.GetGateways(&gateways, filter); err != nil {
		return nil, nil, err
	}

	return &gateways, p, nil
}
