package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"testing"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

func FuzzPaginate(f *testing.F) {
	f.Add("1", 100, 10)
	f.Add("5", 0, 50)
	f.Add("10", 250, 50)

	f.Fuzz(func(t *testing.T, pageStr string, n, per int) {
		p, err := paginate(pageStr, n, per)
		if err != nil {
			// TODO: verify pageStr is invalid int
			return
		}
		if p == nil {
			t.Fatal("p is nil")
		}
		if p.Page < 1 || p.Page > p.Count {
			t.Fatalf("p.Page is %d (count %d)", p.Page, p.Count)
		}
		if p.Count <= 0 {
			t.Fatalf("p.Count is %d", p.Count)
		}
		if p.Offset < 0 || p.Offset > n {
			t.Fatalf("p.Offset is %d (n=%d, per=%d)", p.Offset, n, per)
		}
		if p.Page == 1 {
			if p.Prev != 0 {
				t.Fatalf("p.Page is %d but p.Prev is not zero (%d)", p.Page, p.Prev)
			}
		} else if p.Prev+1 != p.Page {
			t.Fatalf("prev %d+1 != %d", p.Prev, p.Page)
		}
		if p.Page == p.Count {
			if p.Next != 0 {
				t.Fatalf("p.Page is %d but p.Next is not zero (%d)", p.Page, p.Next)
			}
		} else if p.Next-1 != p.Page {
			t.Fatalf("next %d-1 != %d", p.Next, p.Page)
		}
	})
}

func FuzzGatewayIndexPaginate(f *testing.F) {
	db := freshDb(f)

	for i := 0; i < 150; i++ {
		b := Gateway{
			Name:      fmt.Sprintf("Name%d", i),
			IpAddress: fmt.Sprintf("IpAddress%d", i),
			Port:      fmt.Sprintf("506%d", i),
		}
		if err := db.Create(&b).Error; err != nil {
			f.Fatalf("error creating gateway: %s", err)
		}
	}

	f.Add(1)
	f.Add(5)
	f.Add(500)

	f.Fuzz(func(t *testing.T, page int) {
		w := httptest.NewRecorder()
		ctx, r := gin.CreateTestContext(w)
		setupRouter(r, db)
		req, err := http.NewRequestWithContext(ctx, "GET",
			fmt.Sprintf("/gateways/?page=%d", page),
			nil,
		)
		if err != nil {
			t.Errorf("got error: %s", err)
		}
		r.ServeHTTP(w, req)
		expected := http.StatusOK
		if page > 10 || page < 1 {
			expected = http.StatusBadRequest
		}
		if expected != w.Code {
			t.Fatalf("expected response code %d, got %d", http.StatusOK, w.Code)
		}
		if expected == http.StatusOK {
			body := w.Body.String()
			fragments := make([]string, 2)
			fragments[0] = "<h1>My Gateways</h1>"
			if page == 4 {
				fragments[0] = `<strong>4</strong>`
			} else {
				fragments[0] = `<a href="/gateways/?page=4">4</a>`
			}
			for _, fragment := range fragments {
				if !strings.Contains(body, fragment) {
					t.Fatalf("expected body to contain '%s', got %s", fragment, body)
				}
			}
		}
	})
}

func TestDefaultRoute(t *testing.T) {
	t.Parallel()

	w := httptest.NewRecorder()
	ctx, r := gin.CreateTestContext(w)
	os.Setenv("PKS_SESSION_KEY", "dummy")
	setupRouter(r, freshDb(t))

	req, err := http.NewRequestWithContext(ctx, "GET", "/", nil)
	if err != nil {
		t.Errorf("got error: %s", err)
	}

	r.ServeHTTP(w, req)
	if http.StatusOK != w.Code {
		t.Fatalf("expected response code %d, got %d", http.StatusOK, w.Code)
	}

	body := w.Body.String()

	expected := "Hello, gin!"

	if expected != strings.Trim(body, " \r\n") {
		t.Fatalf("expected response body '%s', got '%s'", expected, body)
	}
} // End TestDefaultRoute

func TestGatewayIndexError(t *testing.T) {
	t.Parallel()

	db := freshDb(t)
	if err := db.Migrator().DropTable(&Gateway{}); err != nil {
		t.Fatalf("got error: %s", err)
	}
	_ = getHasStatus(t, db, "/gateways/", http.StatusInternalServerError)
}

func TestGatewayIndexTable(t *testing.T) {
	t.Parallel()
	tcs := []struct {
		name  string
		count int
	}{
		{"empty", 0},
		{"single", 1},
		{"multiple", 10},
	}

	for i := range tcs {
		tc := &tcs[i]
		t.Run(tc.name, func(t *testing.T) {
			t.Parallel()
			db := freshDb(t)
			gateways := createGateways(t, db, tc.count)

			w := getHasStatus(t, db, "/gateways/", http.StatusOK)
			body := w.Body.String()
			fragments := []string{
				"<h2>My Gateways</h2>",
			}
			for _, gateway := range gateways {
				fragments = append(fragments,
					fmt.Sprintf("<span class=\"name\">%s</span>",
						gateway.Name))
				fragments = append(fragments,
					fmt.Sprintf("<span class=\"cidr\">%s:%s</span>",
						gateway.IpAddress, gateway.Port))
			}
			bodyHasFragments(t, body, fragments)
		})
	}
}

func TestGatewayIndex(t *testing.T) {
	t.Parallel()
	db := freshDb(t)
	gateways := createGateways(t, db, 2)

	w := getHasStatus(t, db, "/gateways/", http.StatusOK)
	body := w.Body.String()
	fragments := []string{
		"<h2>My Gateways</h2>",
		fmt.Sprintf("<span class=\"name\">%s</span>", gateways[0].Name),
		fmt.Sprintf("<span class=\"cidr\">%s:%s</span>", gateways[0].IpAddress, gateways[0].Port),
		fmt.Sprintf("<span class=\"name\">%s</span>", gateways[1].Name),
		fmt.Sprintf("<span class=\"cidr\">%s:%s</span>", gateways[1].IpAddress, gateways[1].Port),
	}
	bodyHasFragments(t, body, fragments)
}

func TestGatewayNewGet(t *testing.T) {
	t.Parallel()
	tcs := []struct {
		name string
	}{
		{"basic"},
	}

	for i := range tcs {
		tc := &tcs[i]
		t.Run(tc.name, func(t *testing.T) {
			t.Parallel()
			db := freshDb(t)
			w := getHasStatus(t, db, "/gateways/new", http.StatusOK)
			body := w.Body.String()
			fragments := []string{
				"<h2>Add a Gateway</h2>",
				`<form action="/gateways/new" method="POST">`,
				`<input type="text" name="name" id="name"`,
				`<input type="text" name="ipaddress" id="ipaddress"`,
				`<input type="text" name="port" id="port"`,
				`<button type="submit"`,
			}
			bodyHasFragments(t, body, fragments)
		})
	}
}

func TestGatewayNewPost(t *testing.T) {
	t.Parallel()

	dropTable := func(t *testing.T, db *gorm.DB) {
		err := db.Migrator().DropTable("gateways")
		if err != nil {
			t.Fatalf("error dropping table 'gateways': %s", err)
		}
	}

	tcs := []struct {
		name      string
		data      gin.H
		setup     func(*testing.T, *gorm.DB)
		status    int
		fragments []string
	}{
		{
			name:   "nominal",
			data:   gin.H{"name": "my gateway", "ipaddress": "10.1.1.1", "port": "5060"},
			status: http.StatusFound,
		},
		{
			// This makes the manual field validation fail because the
			// ipaddress is empty.
			name:   "empty_ipaddress",
			data:   gin.H{"name": "my gateway", "port": "5060"},
			status: http.StatusBadRequest,
			fragments: []string{
				"IpAddress is required, but was empty",
			},
		},
		{
			// This makes the manual field validation fail because the
			// name is empty.
			name:   "empty_name",
			data:   gin.H{"ipaddress": "10.1.1.1", "port": "5060"},
			status: http.StatusBadRequest,
			fragments: []string{
				"Name is required, but was empty",
			},
		},
		{
			// This makes the manual field validation fail because the
			// port is empty.
			name:   "empty_port",
			data:   gin.H{"name": "my gateway", "ipaddress": "10.1.1.1"},
			status: http.StatusBadRequest,
			fragments: []string{
				"Port is required, but was empty",
			},
		},
		{
			// This makes the manual field validation fail because both
			// name and ipaddress are empty.
			name:   "empty",
			data:   gin.H{},
			status: http.StatusBadRequest,
			fragments: []string{
				"Name is required, but was empty",
				"IpAddress is required, but was empty",
				"Port is required, but was empty",
			},
		},
		{
			name:   "db_error",
			data:   gin.H{"name": "my gateway", "ipaddress": "10.1.1.1", "port": "5060"},
			setup:  dropTable,
			status: http.StatusInternalServerError,
		},
	}

	for i := range tcs {
		tc := &tcs[i]
		t.Run(tc.name, func(t *testing.T) {
			t.Parallel()
			db := freshDb(t)
			if tc.setup != nil {
				tc.setup(t, db)
			}
			w := postHasStatus(t, db, "/gateways/new", &tc.data,
				tc.status)

			if tc.fragments != nil {
				body := w.Body.String()
				bodyHasFragments(t, body, tc.fragments)
			}

			// NEW CHECKS HERE
			if tc.status == http.StatusFound {
				// Make sure the record is in the db.
				gateways := []Gateway{}
				result := db.Find(&gateways)
				if result.Error != nil {
					t.Fatalf("error fetching gateways: %s", result.Error)
				}
				if result.RowsAffected != 1 {
					t.Fatalf("expected 1 row affected, got %d",
						result.RowsAffected)
				}
				if tc.data["name"] != gateways[0].Name {
					t.Fatalf("expected name '%s', got '%s",
						tc.data["name"], gateways[0].Name)
				}
				if tc.data["ipaddress"] != gateways[0].IpAddress {
					t.Fatalf("expected ipaddress '%s', got '%s",
						tc.data["ipaddress"], gateways[0].IpAddress)
				}
				if tc.data["port"] != gateways[0].Port {
					t.Fatalf("expected iport '%s', got '%s",
						tc.data["port"], gateways[0].Port)
				}

				// Check the redirect location.
				url, err := w.Result().Location()
				if err != nil {
					t.Fatalf("location check error: %s", err)
				}

				if "/gateways/" != url.String() {
					t.Errorf("expected location '/gateways/', got '%s'",
						url.String())
				}

				// Check the flash message in the redirect page.
				w := getCookieHasStatus(t, db, url.String(), w.Result(), http.StatusOK)
				fragments := []string{
					fmt.Sprintf("New gateway &#39;%s&#39; saved successfully.", gateways[0].Name),
				}
				bodyHasFragments(t, w.Body.String(), fragments)

			}
		})
	}
}

func getCookieHasStatus(t *testing.T, db *gorm.DB, path string, r *http.Response, status int) *httptest.ResponseRecorder {
	t.Helper()
	w := httptest.NewRecorder()
	ctx, router := gin.CreateTestContext(w)
	os.Setenv("PKS_SESSION_KEY", "dummy")
	setupRouter(router, db)
	req, err := http.NewRequestWithContext(ctx, "GET", path, nil)
	if err != nil {
		t.Errorf("got error: %s", err)
	}
	if r != nil {
		req.Header["Cookie"] = r.Header["Set-Cookie"]
	}
	router.ServeHTTP(w, req)
	if status != w.Code {
		t.Errorf("expected response code %d, got %d", status, w.Code)
	}
	return w
}
