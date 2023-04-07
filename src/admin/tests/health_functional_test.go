package test

import (
	"io"
	"net/http"
)

func (s *TestSuiteEnv) TestHealth() {
	c := http.Client{}

	r, _ := c.Get("http://localhost:3000/v1/health")
	body, _ := io.ReadAll(r.Body)

	s.Equal(http.StatusOK, r.StatusCode)
	s.JSONEq(`{"data":null,"error":false,"message":"Working fine !"}`, string(body))
}
