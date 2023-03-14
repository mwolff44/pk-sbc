package config

import (
	"os"
)

const (
	// LogLevel var defines the log details
	LogLevel      = "info"
	goEnvironment = "GO_ENVIRONMENT"
	production    = "production"
)

// IsProduction function determine the status of the app
func IsProduction() bool {
	return os.Getenv(goEnvironment) == production
}
