package filters

import (
	"log"
	"testing"
)

func FuzzPaginate(f *testing.F) {
	f.Add(1, 100, 10)
	//f.Add(5, 0, 50)
	f.Add(10, 250, 50)

	f.Fuzz(func(t *testing.T, page int, totalRecords int, pageSize int) {

		p, err := Paginate(page, totalRecords, pageSize)
		log.Printf("P is %v", p)
		if err != nil {
			// TODO: verify pageStr is invalid int
			return
		}
		if p == nil {
			t.Fatal("p is nil")
		}
		if p.CurrentPage > p.LastPage {
			t.Fatalf("p.CurrentPage is %d (count %d)", p.CurrentPage, p.LastPage)
		}
		if p.LastPage <= 0 {
			t.Fatalf("p.LastPage is %d", p.LastPage)
		}
		if p.CurrentPage == 1 {
			if p.Prev != 1 {
				t.Fatalf("p.CurrentPage is %d but p.Prev is not zero (%d)", p.CurrentPage, p.Prev)
			}
		} else if p.Prev+1 != p.CurrentPage {
			t.Fatalf("prev %d+1 != %d", p.Prev, p.CurrentPage)
		}
		if p.CurrentPage == p.TotalRecords {
			if p.Next != 0 {
				t.Fatalf("p.CurrentPage is %d but p.Next is not zero (%d)", p.CurrentPage, p.Next)
			}
		} else if p.Next-1 != p.CurrentPage {
			t.Fatalf("next %d-1 != %d", p.Next, p.CurrentPage)
		}
	})
}
