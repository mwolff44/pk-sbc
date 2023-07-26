package test

import (
	"io"
	"net/http"
)

func (s *TestSuiteEnv) TestGateway() {
	c := http.Client{}

	r, _ := c.Get("http://localhost:3000/v1/gateways/1")
	body, _ := io.ReadAll(r.Body)

	s.Equal(http.StatusOK, r.StatusCode)
	s.JSONEq(`{"data":{"id":1,"created_at":"2023-03-24T19:20:48.689322432+01:00","updated_at":"2023-03-24T19:20:48.689370399+01:00","name":"Licensed Cotton Sausages","ip_address":"76.41.217.75","port":1035,"protocol":"tcp"},"error":false,"message":"Requested gateway"}`, string(body))
}
