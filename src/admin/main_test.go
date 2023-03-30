package main

import (
	"fmt"
	"net/http"
	"os"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
	"pks.pyfreebilling.com/app"
)

// This function is used to do setup before executing the test functions
func TestMain(m *testing.M) {
	fmt.Println("About to start the application for functional tests")

	//Set Gin to Test Mode
	gin.SetMode(gin.TestMode)

	// Start application
	go app.StartApp()

	// Run the other tests
	os.Exit(m.Run())
}

func TestGetHealthOK(t *testing.T) {

	// Init:

	// Execution:
	response, err := http.Get("http://localhost:3000/v1/health")

	// Validation:
	assert.Nil(t, err)
	assert.NotNil(t, response)
	/* 	bytes, _ := ioutil.ReadAll(response.Body)

	   	var apiErr utils.ApplicationError
	   	err = json.Unmarshal(bytes, &apiErr)
	   	assert.Nil(t, err)

	   	assert.EqualValues(t, http.StatusNotFound, apiErr.StatusCode)
	   	assert.EqualValues(t, "not_found", apiErr.Code)
	   	assert.EqualValues(t, "no country with id AR", apiErr.Message) */
}
