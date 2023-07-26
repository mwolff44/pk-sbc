package config

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestIsProductionn(t *testing.T) {
	assert.EqualValues(t, false, IsProduction())
}
