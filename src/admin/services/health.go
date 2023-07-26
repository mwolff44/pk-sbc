package services

import (
	"fmt"
)

const (
	health = "Working fine !"
)

type healthService struct{}

type healthServiceInterface interface {
	Health() (string, error)
}

// HealthService
var (
	HealthService healthServiceInterface
)

func init() {
	HealthService = &healthService{}
}

// Health returns the service state
func (s *healthService) Health() (string, error) {
	fmt.Println("Working fine !")
	return health, nil
}
