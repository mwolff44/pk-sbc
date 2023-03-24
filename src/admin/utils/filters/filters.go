package filters

import (
	"errors"
	"math"
	"strings"
)

// Filters defines the struct of query
type Filters struct {
	Page         int    `form:"page,default=1" binding:"omitempty,min=1,max=10_000_000"`
	PageSize     int    `form:"page_size,default=5" binding:"omitempty,min=5,max=100"`
	Sort         string `form:"sort"`
	SortSafelist []string
}

// Pargination is the object return defining the pagination details of a list of objects
type Pagination struct {
	CurrentPage  int `json:"current_page,omitempty"`
	PageSize     int `json:"page_size,omitempty"`
	LastPage     int `json:"last_page,omitempty"`
	TotalRecords int `json:"total_records,omitempty"`
	Prev         int `json:"prev_page,omitempty"`
	Next         int `json:"next_page,omitempty"`
}

func (f Filters) Limit() int {
	return f.PageSize
}

func (f *Filters) Offset() int {
	return (f.Page - 1) * f.PageSize
}

func (f Filters) SortColumn() string {
	for _, safeValue := range f.SortSafelist {
		if f.Sort == safeValue {
			return strings.TrimPrefix(f.Sort, "-")
		}
	}

	panic("unsafe sort parameter: " + f.Sort)
}

func (f Filters) SortDirection() string {
	if strings.HasPrefix(f.Sort, "-") {
		return "desc"
	}

	return "asc"
}

func (f Filters) SortOrder() string {
	return f.SortColumn() + " " + f.SortDirection()
}

func (f *Filters) GetSort() string {
	if f.Sort == "" {
		f.Sort = "id"
	}
	return f.Sort
}

func prev(currentPage int) int {
	if currentPage > 1 {
		return currentPage - 1
	}
	return currentPage
}

func next(currentPage int, lastPage int) int {
	if currentPage < lastPage {
		return currentPage + 1
	}
	return lastPage
}

func lastPage(totalRecords int, pageSize int) int {
	lastPage := int(math.Ceil(float64(totalRecords) / float64(pageSize)))
	if lastPage == 0 {
		return 1
	}
	return lastPage
}

func Paginate(page int, totalRecords int, pageSize int) (*Pagination, error) {
	if totalRecords == 0 {
		return &Pagination{}, nil
	}
	lastPageNb := lastPage(totalRecords, pageSize)
	if page > lastPageNb {
		return nil, errors.New("invalid page number")
	}

	return &Pagination{
		CurrentPage:  page,
		PageSize:     pageSize,
		LastPage:     lastPageNb,
		TotalRecords: totalRecords,
		Prev:         prev(page),
		Next:         next(page, lastPageNb),
	}, nil

}
