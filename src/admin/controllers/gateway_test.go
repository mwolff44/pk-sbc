package controllers

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"net/http/httptest"
	"net/url"
	"strconv"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
	"gorm.io/gorm"
	"pks.pyfreebilling.com/models"
	"pks.pyfreebilling.com/services"
	"pks.pyfreebilling.com/utils"
	"pks.pyfreebilling.com/utils/filters"
)

var (
	listGatewaysFunc   func(filters.Filters) (*models.Gateways, *filters.Pagination, error)
	createGatewayFunc  func(models.Gateway) (*models.Gateway, error)
	getGatewayByIDFunc func(id int64) (*models.Gateway, error)
	updateGatewayFunc  func(models.Gateway) (*models.Gateway, error)
	deleteGatewayFunc  func(id int64) error
)

type gatewayServiceMock struct{}

func (*gatewayServiceMock) ListGateways(filter filters.Filters) (*models.Gateways, *filters.Pagination, error) {
	return listGatewaysFunc(filter)
}

func (*gatewayServiceMock) CreateGateway(gateway models.Gateway) (*models.Gateway, error) {
	return createGatewayFunc(gateway)
}

func (*gatewayServiceMock) GetGateway(id int64) (*models.Gateway, error) {
	return getGatewayByIDFunc(id)
}

func (*gatewayServiceMock) UpdateGateway(gateway models.Gateway) (*models.Gateway, error) {
	return updateGatewayFunc(gateway)
}

func (*gatewayServiceMock) DeleteGateway(id int64) error {
	return deleteGatewayFunc(id)
}

func TestGetGateways(t *testing.T) {
	// Define a structure for specifying input and output data of a single test case.
	date := time.Now()
	tests := []struct {
		description          string
		svcModel             *models.Gateways
		svcPagination        *filters.Pagination
		svcError             error
		filter               *filters.Filters
		expectedResponseCode int
		expectedResponse     utils.PaginatedResponseHTTP
	}{
		{
			description: "Get a gateway list",
			svcModel: &models.Gateways{
				{
					ID:        1,
					CreatedAt: date,
					UpdatedAt: date,
					Name:      "Licensed Cotton Sausages",
					IpAddress: "76.41.217.75",
					Port:      1035,
					Protocol:  "tcp",
				},
			},
			svcPagination: &filters.Pagination{
				CurrentPage:  2,
				PageSize:     10,
				LastPage:     1,
				TotalRecords: 1,
			},
			svcError: nil,
			filter: &filters.Filters{
				Page:     2,
				PageSize: 10,
				Sort:     "-id",
			},
			expectedResponseCode: http.StatusOK,
			expectedResponse: utils.PaginatedResponseHTTP{
				Error:   false,
				Message: "Gateway list",
				Data: &models.Gateways{
					{
						ID:        1,
						CreatedAt: date,
						UpdatedAt: date,
						Name:      "Licensed Cotton Sausages",
						IpAddress: "76.41.217.75",
						Port:      1035,
						Protocol:  "tcp",
					},
				},
				Pagination: filters.Pagination{
					CurrentPage:  1,
					PageSize:     5,
					LastPage:     1,
					TotalRecords: 1,
				},
			},
		},
		{
			description:   "Wrong param : page 0",
			svcModel:      nil,
			svcPagination: nil,
			svcError:      nil,
			filter: &filters.Filters{
				Page:     0,
				PageSize: 1,
				Sort:     "id",
			},
			expectedResponseCode: http.StatusBadRequest,
			expectedResponse: utils.PaginatedResponseHTTP{
				Error:   true,
				Message: "Invalid inputs. Please check your inputs",
				Data:    nil,
			},
		},
		{
			description:   "Invalid page number",
			svcModel:      nil,
			svcPagination: nil,
			svcError:      errors.New("invalid page number"),
			filter: &filters.Filters{
				Page:     10,
				PageSize: 5,
				Sort:     "id",
			},
			expectedResponseCode: http.StatusBadRequest,
			expectedResponse: utils.PaginatedResponseHTTP{
				Error:   true,
				Message: "Pagination error : invalid page number",
				Data:    nil,
			},
		},
		{
			description:   "Generic service error",
			svcModel:      nil,
			svcPagination: nil,
			svcError:      errors.New("not invalid page number"),
			filter: &filters.Filters{
				Page:     10,
				PageSize: 5,
				Sort:     "id",
			},
			expectedResponseCode: http.StatusInternalServerError,
			expectedResponse: utils.PaginatedResponseHTTP{
				Error:   true,
				Message: "Error in getting gateway list",
				Data:    nil,
			},
		},
		{
			description: "Wrong param : sort data => get default",
			svcModel: &models.Gateways{
				{
					ID:        1,
					CreatedAt: date,
					UpdatedAt: date,
					Name:      "Licensed Cotton Sausages",
					IpAddress: "76.41.217.75",
					Port:      1035,
					Protocol:  "tcp",
				},
			},
			svcPagination: &filters.Pagination{
				CurrentPage:  1,
				PageSize:     10,
				LastPage:     1,
				TotalRecords: 1,
			},
			svcError: nil,
			filter: &filters.Filters{
				Page:     1,
				PageSize: 10,
				Sort:     "z",
			},
			expectedResponseCode: http.StatusOK,
			expectedResponse: utils.PaginatedResponseHTTP{
				Error:   false,
				Message: "Gateway list",
				Data: &models.Gateways{
					{
						ID:        1,
						CreatedAt: date,
						UpdatedAt: date,
						Name:      "Licensed Cotton Sausages",
						IpAddress: "76.41.217.75",
						Port:      1035,
						Protocol:  "tcp",
					},
				},
				Pagination: filters.Pagination{
					CurrentPage:  1,
					PageSize:     5,
					LastPage:     1,
					TotalRecords: 1,
				},
			},
		},
		{
			description:   "Wrong param : pageSize 0",
			svcModel:      nil,
			svcPagination: nil,
			svcError:      nil,
			filter: &filters.Filters{
				Page:     1,
				PageSize: 0,
				Sort:     "id",
			},
			expectedResponseCode: http.StatusBadRequest,
			expectedResponse: utils.PaginatedResponseHTTP{
				Error:   true,
				Message: "Invalid inputs. Please check your inputs",
				Data:    nil,
			},
		},
	}

	for _, test := range tests {
		t.Run(test.description, func(t *testing.T) {
			listGatewaysFunc = func(filter filters.Filters) (*models.Gateways, *filters.Pagination, error) {
				return test.svcModel, test.svcPagination, test.svcError
			}
			services.GatewaysService = &gatewayServiceMock{}

			response := httptest.NewRecorder()
			c, _ := gin.CreateTestContext(response)

			c.Request, _ = http.NewRequest(http.MethodGet, "/", nil)

			/* c.Params = gin.Params{
				{Key: "page", Value: strconv.Itoa(test.filter.Page)},
				{Key: "page_size", Value: strconv.Itoa(test.filter.PageSize)},
				{Key: "sort", Value: test.filter.Sort},
			} */

			// set query params
			u := url.Values{}
			u.Add("page", strconv.Itoa(test.filter.Page))
			u.Add("page_size", strconv.Itoa(test.filter.PageSize))
			u.Add("sort", test.filter.Sort)
			c.Request.URL.RawQuery = u.Encode()

			fmt.Printf("params : %v", c.Params)

			GetGateways(c)

			assert.EqualValues(t, test.expectedResponseCode, response.Code)

			var gwResp utils.ResponseHTTP
			err := json.Unmarshal(response.Body.Bytes(), &gwResp)
			assert.Nil(t, err)

			assert.EqualValues(t, test.expectedResponse.Error, gwResp.Error)
			assert.EqualValues(t, test.expectedResponse.Message, gwResp.Message)

			if test.expectedResponse.Data != nil {
				dataJson, _ := json.Marshal(test.expectedResponse.Data)
				respJson, _ := json.Marshal(gwResp.Data)
				assert.JSONEq(t, string(dataJson), string(respJson))
			}
		})
	}

}

func TestCreateGateway(t *testing.T) {
	// Define a structure for specifying input and output data of a single test case.
	date := time.Now()
	tests := []struct {
		description          string
		g                    *models.Gateway
		svcModel             *models.Gateway
		svcError             error
		expectedResponseCode int
		expectedResponse     utils.ResponseHTTP
	}{
		{
			description: "Create a valid gateway item",
			g: &models.Gateway{
				Name:      "Licensed Cotton Sausages",
				IpAddress: "76.41.217.75",
				Port:      1035,
				Protocol:  "tcp",
			},
			svcModel: &models.Gateway{
				ID:        1,
				CreatedAt: date,
				UpdatedAt: date,
				Name:      "Licensed Cotton Sausages",
				IpAddress: "76.41.217.75",
				Port:      1035,
				Protocol:  "tcp",
			},
			svcError:             nil,
			expectedResponseCode: http.StatusCreated,
			expectedResponse: utils.ResponseHTTP{
				Error:   false,
				Message: "Gateway created",
				Data: &models.Gateway{
					ID:        1,
					CreatedAt: date,
					UpdatedAt: date,
					Name:      "Licensed Cotton Sausages",
					IpAddress: "76.41.217.75",
					Port:      1035,
					Protocol:  "tcp",
				},
			},
		},
		{
			description: "No Name field",
			g: &models.Gateway{
				IpAddress: "76.41.217.75",
				Port:      1035,
				Protocol:  "tcp",
			},
			svcModel:             nil,
			svcError:             errors.New("Invalid json body. Please check your inputs"),
			expectedResponseCode: http.StatusBadRequest,
			expectedResponse: utils.ResponseHTTP{
				Error:   true,
				Message: "Invalid json body. Please check your inputs",
			},
		},
		{
			description: "Error creating gateway",
			g: &models.Gateway{
				Name:      "Licensed Cotton Sausages",
				IpAddress: "76.41.217.75",
				Port:      1035,
				Protocol:  "tcp",
			},
			svcModel:             nil,
			svcError:             errors.New("Error in creating gateway"),
			expectedResponseCode: http.StatusInternalServerError,
			expectedResponse: utils.ResponseHTTP{
				Error:   true,
				Message: "Error in creating gateway",
			},
		},
	}

	// Mock GatewayService methods

	for _, test := range tests {
		t.Run(test.description, func(t *testing.T) {
			createGatewayFunc = func(gw models.Gateway) (*models.Gateway, error) {
				return test.svcModel, test.svcError
			}
			services.GatewaysService = &gatewayServiceMock{}

			response := httptest.NewRecorder()
			c, _ := gin.CreateTestContext(response)

			body, _ := json.Marshal(test.g)

			c.Request, _ = http.NewRequest(http.MethodPost, "/", bytes.NewBuffer(body))

			/* 	body, _ := json.Marshal(test.g)
			c.Request.Body, _ = io.ReadCloser(body) */

			CreateGateway(c)

			assert.EqualValues(t, test.expectedResponseCode, response.Code)

			var gwResp utils.ResponseHTTP
			err := json.Unmarshal(response.Body.Bytes(), &gwResp)
			assert.Nil(t, err)

			assert.EqualValues(t, test.expectedResponse.Error, gwResp.Error)
			assert.EqualValues(t, test.expectedResponse.Message, gwResp.Message)

			if test.expectedResponse.Data != nil {
				assert.Contains(t, response.Header(), "Location")
				dataJson, _ := json.Marshal(test.expectedResponse.Data)
				respJson, _ := json.Marshal(gwResp.Data)
				assert.JSONEq(t, string(dataJson), string(respJson))
			}
		})
	}
}

func TestGetGatewayByID(t *testing.T) {
	// Define a structure for specifying input and output data of a single test case.
	date := time.Now()
	tests := []struct {
		description          string
		g                    *models.Gateway
		svcError             error
		param                string
		expectedResponseCode int
		expectedResponse     utils.ResponseHTTP
	}{
		{
			description: "Get a valid gateway item",
			g: &models.Gateway{
				ID:        1,
				CreatedAt: date,
				UpdatedAt: date,
				Name:      "Licensed Cotton Sausages",
				IpAddress: "76.41.217.75",
				Port:      1035,
				Protocol:  "tcp",
			},
			svcError:             nil,
			param:                "1",
			expectedResponseCode: http.StatusOK,
			expectedResponse: utils.ResponseHTTP{
				Error:   false,
				Message: "Requested gateway",
				Data: &models.Gateway{
					ID:        1,
					CreatedAt: date,
					UpdatedAt: date,
					Name:      "Licensed Cotton Sausages",
					IpAddress: "76.41.217.75",
					Port:      1035,
					Protocol:  "tcp",
				},
			},
		},
		{
			description:          "Wrong Param : not a number",
			g:                    nil,
			svcError:             nil,
			param:                "a",
			expectedResponseCode: http.StatusBadRequest,
			expectedResponse: utils.ResponseHTTP{
				Error:   true,
				Message: "Invalid input. Please check your inputs",
				Data:    nil,
			},
		},
		{
			description:          "Test low limit : 0 as ID",
			g:                    nil,
			svcError:             nil,
			param:                "0",
			expectedResponseCode: http.StatusBadRequest,
			expectedResponse: utils.ResponseHTTP{
				Error:   true,
				Message: "Invalid input. Please check your inputs",
				Data:    nil,
			},
		},
		{
			description:          "Test high limit : 9223372036854775808 as ID",
			g:                    nil,
			svcError:             nil,
			param:                "9223372036854775808",
			expectedResponseCode: http.StatusBadRequest,
			expectedResponse: utils.ResponseHTTP{
				Error:   true,
				Message: "Invalid input. Please check your inputs",
				Data:    nil,
			},
		},
		{
			description:          "request a non existing ID",
			g:                    nil,
			svcError:             gorm.ErrRecordNotFound,
			param:                "2",
			expectedResponseCode: http.StatusBadRequest,
			expectedResponse: utils.ResponseHTTP{
				Error:   true,
				Message: "id does not exists in database",
				Data:    nil,
			},
		},
		{
			description:          "Service other error",
			g:                    nil,
			svcError:             errors.New("internal service error"),
			param:                "2",
			expectedResponseCode: http.StatusInternalServerError,
			expectedResponse: utils.ResponseHTTP{
				Error:   true,
				Message: "internal service error",
				Data:    nil,
			},
		},
	}

	// Mock GatewayService methods

	for _, test := range tests {
		t.Run(test.description, func(t *testing.T) {
			getGatewayByIDFunc = func(id int64) (*models.Gateway, error) {
				return test.g, test.svcError
			}
			services.GatewaysService = &gatewayServiceMock{}

			response := httptest.NewRecorder()
			c, _ := gin.CreateTestContext(response)

			c.Request, _ = http.NewRequest(http.MethodGet, "/", nil)

			c.Params = gin.Params{
				{Key: "id", Value: test.param},
			}

			GetGatewayByID(c)

			assert.EqualValues(t, test.expectedResponseCode, response.Code)

			var gwResp utils.ResponseHTTP
			err := json.Unmarshal(response.Body.Bytes(), &gwResp)
			assert.Nil(t, err)

			assert.EqualValues(t, test.expectedResponse.Error, gwResp.Error)
			assert.EqualValues(t, test.expectedResponse.Message, gwResp.Message)

			if test.expectedResponse.Data != nil {
				dataJson, _ := json.Marshal(test.expectedResponse.Data)
				respJson, _ := json.Marshal(gwResp.Data)
				assert.JSONEq(t, string(dataJson), string(respJson))
			}
		})
	}
}

func TestUpdateGateway(t *testing.T) {
	// Define a structure for specifying input and output data of a single test case.
	date := time.Now()
	tests := []struct {
		description          string
		g                    *models.Gateway
		svcModel             *models.Gateway
		svcGetError          error
		svcError             error
		param                string
		expectedResponseCode int
		expectedResponse     utils.ResponseHTTP
	}{
		{
			description: "Update a valid gateway item",
			g: &models.Gateway{
				ID:        1,
				Name:      "Licensed Cotton Sausages",
				IpAddress: "76.41.217.75",
				Port:      1035,
				Protocol:  "tcp",
			},
			svcModel: &models.Gateway{
				ID:        1,
				CreatedAt: date,
				UpdatedAt: date,
				Name:      "Licensed Cotton Sausages",
				IpAddress: "76.41.217.75",
				Port:      1035,
				Protocol:  "tcp",
			},
			svcGetError:          nil,
			svcError:             nil,
			param:                "1",
			expectedResponseCode: http.StatusOK,
			expectedResponse: utils.ResponseHTTP{
				Error:   false,
				Message: "Gateway updated",
				Data: &models.Gateway{
					ID:        1,
					CreatedAt: date,
					UpdatedAt: date,
					Name:      "Licensed Cotton Sausages",
					IpAddress: "76.41.217.75",
					Port:      1035,
					Protocol:  "tcp",
				},
			},
		},
		{
			description: "Wrong ID",
			g: &models.Gateway{
				ID:        1,
				Name:      "Licensed Cotton Sausages",
				IpAddress: "76.41.217.75",
				Port:      1035,
				Protocol:  "tcp",
			},
			svcModel: &models.Gateway{
				ID:        1,
				CreatedAt: date,
				UpdatedAt: date,
				Name:      "Licensed Cotton Sausages",
				IpAddress: "76.41.217.75",
				Port:      1035,
				Protocol:  "tcp",
			},
			svcGetError:          errors.New("Invalid input. Please check your inputs"),
			svcError:             nil,
			param:                "0",
			expectedResponseCode: http.StatusBadRequest,
			expectedResponse: utils.ResponseHTTP{
				Error:   true,
				Message: "Invalid input. Please check your inputs",
			},
		},
		{
			description: "Gateway not found",
			g: &models.Gateway{
				ID:        2,
				Name:      "Licensed Cotton Sausages",
				IpAddress: "76.41.217.75",
				Port:      1035,
				Protocol:  "tcp",
			},
			svcModel: &models.Gateway{
				ID:        2,
				CreatedAt: date,
				UpdatedAt: date,
				Name:      "Licensed Cotton Sausages",
				IpAddress: "76.41.217.75",
				Port:      1035,
				Protocol:  "tcp",
			},
			svcGetError:          errors.New("Gateway not found"),
			svcError:             nil,
			param:                "2",
			expectedResponseCode: http.StatusNotFound,
			expectedResponse: utils.ResponseHTTP{
				Error:   true,
				Message: "Gateway not found",
			},
		},
		{
			description: "No Name field",
			g: &models.Gateway{
				IpAddress: "76.41.217.75",
				Port:      1035,
				Protocol:  "tcp",
			},
			svcModel:             nil,
			svcGetError:          errors.New(""),
			svcError:             errors.New("Invalid json body. Please check your inputs"),
			param:                "1",
			expectedResponseCode: http.StatusBadRequest,
			expectedResponse: utils.ResponseHTTP{
				Error:   true,
				Message: "Invalid json body. Please check your inputs",
			},
		},
		{
			description: "Error updating gateway",
			g: &models.Gateway{
				Name:      "Licensed Cotton Sausages",
				IpAddress: "76.41.217.75",
				Port:      1035,
				Protocol:  "tcp",
			},
			svcModel:             nil,
			svcGetError:          nil,
			svcError:             errors.New("Error in updating gateway"),
			param:                "1",
			expectedResponseCode: http.StatusInternalServerError,
			expectedResponse: utils.ResponseHTTP{
				Error:   true,
				Message: "Error in updating gateway",
			},
		},
	}

	// Mock GatewayService methods

	for _, test := range tests {
		t.Run(test.description, func(t *testing.T) {
			updateGatewayFunc = func(gw models.Gateway) (*models.Gateway, error) {
				return test.svcModel, test.svcError
			}
			getGatewayByIDFunc = func(id int64) (*models.Gateway, error) {
				return nil, test.svcGetError
			}
			services.GatewaysService = &gatewayServiceMock{}

			response := httptest.NewRecorder()
			c, _ := gin.CreateTestContext(response)

			body, _ := json.Marshal(test.g)

			c.Request, _ = http.NewRequest(http.MethodPut, "/", bytes.NewBuffer(body))

			c.Params = gin.Params{
				{Key: "id", Value: test.param},
			}

			UpdateGateway(c)

			assert.EqualValues(t, test.expectedResponseCode, response.Code)

			var gwResp utils.ResponseHTTP
			err := json.Unmarshal(response.Body.Bytes(), &gwResp)
			assert.Nil(t, err)

			assert.EqualValues(t, test.expectedResponse.Error, gwResp.Error)
			assert.EqualValues(t, test.expectedResponse.Message, gwResp.Message)

			if test.expectedResponse.Data != nil {
				dataJson, _ := json.Marshal(test.expectedResponse.Data)
				respJson, _ := json.Marshal(gwResp.Data)
				assert.JSONEq(t, string(dataJson), string(respJson))
			}
		})
	}
}

func TestDeleteGateway(t *testing.T) {
	// Define a structure for specifying input and output data of a single test case.
	tests := []struct {
		description          string
		svcError             error
		param                string
		expectedResponseCode int
		expectedResponse     utils.ResponseHTTP
	}{
		{
			description:          "Get a valid gateway item",
			svcError:             nil,
			param:                "1",
			expectedResponseCode: http.StatusOK,
			expectedResponse: utils.ResponseHTTP{
				Error:   false,
				Message: "Gateway successfully deleted",
				Data:    nil,
			},
		},
		{
			description:          "Wrong Param : not a number",
			svcError:             nil,
			param:                "a",
			expectedResponseCode: http.StatusBadRequest,
			expectedResponse: utils.ResponseHTTP{
				Error:   true,
				Message: "Invalid input. Please check your inputs",
				Data:    nil,
			},
		},
		{
			description:          "Test low limit : 0 as ID",
			svcError:             nil,
			param:                "0",
			expectedResponseCode: http.StatusBadRequest,
			expectedResponse: utils.ResponseHTTP{
				Error:   true,
				Message: "Invalid input. Please check your inputs",
				Data:    nil,
			},
		},
		{
			description:          "Test high limit : 9223372036854775808 as ID",
			svcError:             nil,
			param:                "9223372036854775808",
			expectedResponseCode: http.StatusBadRequest,
			expectedResponse: utils.ResponseHTTP{
				Error:   true,
				Message: "Invalid input. Please check your inputs",
				Data:    nil,
			},
		},
		{
			description:          "request a non existing ID",
			svcError:             gorm.ErrRecordNotFound,
			param:                "2",
			expectedResponseCode: http.StatusBadRequest,
			expectedResponse: utils.ResponseHTTP{
				Error:   true,
				Message: "id does not exists in database",
				Data:    nil,
			},
		},
		{
			description:          "Service other error",
			svcError:             errors.New("internal service error"),
			param:                "2",
			expectedResponseCode: http.StatusInternalServerError,
			expectedResponse: utils.ResponseHTTP{
				Error:   true,
				Message: "internal service error",
				Data:    nil,
			},
		},
	}

	// Mock GatewayService methods

	for _, test := range tests {
		t.Run(test.description, func(t *testing.T) {
			deleteGatewayFunc = func(id int64) error {
				return test.svcError
			}
			services.GatewaysService = &gatewayServiceMock{}

			response := httptest.NewRecorder()
			c, _ := gin.CreateTestContext(response)

			c.Request, _ = http.NewRequest(http.MethodDelete, "/", nil)

			c.Params = gin.Params{
				{Key: "id", Value: test.param},
			}

			DeleteGateway(c)

			assert.EqualValues(t, test.expectedResponseCode, response.Code)

			var gwResp utils.ResponseHTTP
			err := json.Unmarshal(response.Body.Bytes(), &gwResp)
			assert.Nil(t, err)

			assert.EqualValues(t, test.expectedResponse.Error, gwResp.Error)
			assert.EqualValues(t, test.expectedResponse.Message, gwResp.Message)
		})
	}
}
