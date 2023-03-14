package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"net/url"
	"os"
	"strings"
	"testing"

	"github.com/gin-gonic/gin"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

func bodyHasFragments(t *testing.T, body string, fragments []string) {
	t.Helper()
	for _, fragment := range fragments {
		if !strings.Contains(body, fragment) {
			t.Fatalf("expected body to contain '%s', got %s", fragment, body)
		}
	}
}

func getHasStatus(t *testing.T, db *gorm.DB, path string, status int) *httptest.ResponseRecorder {
	t.Helper()

	w := httptest.NewRecorder()
	ctx, router := gin.CreateTestContext(w)
	setupRouter(router, db)

	req, err := http.NewRequestWithContext(ctx, "GET", path, nil)
	if err != nil {
		t.Errorf("got error: %s", err)
	}
	router.ServeHTTP(w, req)
	if status != w.Code {
		t.Errorf("expected response code %d, got %d", status, w.Code)
	}
	return w
}

func postHasStatus(t *testing.T, db *gorm.DB, path string,
	h *gin.H, status int) *httptest.ResponseRecorder {

	t.Helper()
	data := url.Values{}
	for k, vi := range *h {
		v := vi.(string)
		data.Set(k, v)
	}

	w := httptest.NewRecorder()
	ctx, router := gin.CreateTestContext(w)
	os.Setenv("PKS_SESSION_KEY", "dummy")
	setupRouter(router, db)

	req, err := http.NewRequestWithContext(ctx, "POST", path,
		strings.NewReader(data.Encode()))
	if err != nil {
		t.Errorf("got error: %s", err)
	}
	req.Header.Add("Content-Type", "application/x-www-form-urlencoded")
	router.ServeHTTP(w, req)
	responseHasCode(t, w, status)
	return w
}

func responseHasCode(t *testing.T, w *httptest.ResponseRecorder,
	expected int) {

	if expected != w.Code {
		t.Errorf("expected response code %d, got %d", expected, w.Code)
	}
}

type testable interface {
	Helper()
	Fatalf(format string, args ...any)
}

func freshDb(t testable, path ...string) *gorm.DB {
	t.Helper()

	var dbUri string

	// Note: path can be specified in an individual test for debugging
	// purposes -- so the db file can be inspected after the test runs.
	// Normally it should be left off so that a truly fresh memory db is
	// used every time.
	if len(path) == 0 {
		dbUri = ":memory:"
	} else {
		dbUri = path[0]
	}

	db, err := gorm.Open(sqlite.Open(dbUri), &gorm.Config{})
	if err != nil {
		t.Fatalf("Error opening memory db: %s", err)
	}
	if err := setupDatabase(db); err != nil {
		t.Fatalf("Error setting up db: %s", err)
	}
	return db
}

func createGateways(t *testing.T, db *gorm.DB, count int) []*Gateway {
	gateways := []*Gateway{}
	t.Helper()
	for i := 0; i < count; i++ {
		b := &Gateway{
			Name:      fmt.Sprintf("Gateway%03d", i),
			IpAddress: fmt.Sprintf("10.0.0.%03d", i),
			Port:      fmt.Sprintf("506%03d", i),
		}
		if err := db.Create(b).Error; err != nil {
			t.Fatalf("error creating gateway: %s", err)
		}
		gateways = append(gateways, b)
	}
	return gateways
}
