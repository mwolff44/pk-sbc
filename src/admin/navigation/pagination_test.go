package navigation

import "testing"

func FuzzPaginate(f *testing.F) {
	f.Add("1", 100, 10)
	f.Add("5", 0, 50)
	f.Add("10", 250, 50)

	f.Fuzz(func(t *testing.T, pageStr string, n, per int) {
		p, err := Paginate(pageStr, n, per)
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
