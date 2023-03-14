package services

import (
	"fmt"

	"pks.pyfreebilling.com/utils/api_errors"
)

const (
	health = "Working fine !"
)

type healthService struct{}

type healthServiceInterface interface {
	Health() (string, *api_errors.ApiError)
}

// HealthService
var (
	HealthService healthServiceInterface
)

func init() {
	HealthService = &healthService{}
}

// HandleHealth returns ok information
func (s *healthService) Health() (string, *api_errors.ApiError) {
	fmt.Println("Working fine !")
	return health, nil
}
