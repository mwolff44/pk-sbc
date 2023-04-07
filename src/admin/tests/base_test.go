package test

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/suite"
)

type TestSuiteEnv struct {
	suite.Suite
	//db *gorm.DB
}

// Tests are run before they start
func (suite *TestSuiteEnv) SetupSuite() {
	fmt.Println("About to start the application for functional tests")

	/*
		 	//Set Gin to Test Mode
			gin.SetMode(gin.TestMode)

			// Start application
			serverReady := make(chan bool)
			go app.StartApp("test.sqlite3")
			<-serverReady
	*/
}

// Running after each test
func (suite *TestSuiteEnv) TearDownTest() {
	//database.ClearTable()
}

// Running after all tests are completed
func (suite *TestSuiteEnv) TearDownSuite() {
	//p, _ := os.FindProcess(syscall.Getpid())
	//p.Signal(syscall.SIGINT)
}

// This gets run automatically by `go test` so we call `suite.Run` inside it
func TestSuite(t *testing.T) {
	// This is what actually runs our suite
	suite.Run(t, new(TestSuiteEnv))
}
