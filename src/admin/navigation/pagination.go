package navigation

import (
	"errors"
	"math"
	"strconv"
)

type Pagination struct {
	Page   int
	Count  int
	Offset int
	Prev   int
	Next   int
}

func (p *Pagination) Pages() []int {
	pages := make([]int, p.Count)
	for i := 0; i < p.Count; i++ {
		pages[i] = i + 1
	}
	return pages
}

func Paginate(pageStr string, n, per int) (*Pagination, error) {
	if n < 0 || per <= 0 {
		return nil, errors.New("invalid quantity or per-page")
	}

	p := &Pagination{}
	var err error
	p.Page, err = strconv.Atoi(pageStr)
	if err != nil {
		return nil, err
	}
	p.Count = int(math.Ceil(float64(n) / float64(per)))
	if p.Count == 0 {
		p.Count = 1
	}
	if p.Page < 1 || p.Page > p.Count {
		return nil, errors.New("invalid page")
	}
	p.Offset = (p.Page - 1) * per

	if p.Page > 1 {
		p.Prev = p.Page - 1
	}
	if p.Page < p.Count {
		p.Next = p.Page + 1
	}

	return p, nil
}
