package main

type Gateway struct {
	ID        uint   `form:"-"`
	Name      string `form:"name" binding:"required"`
	IpAddress string `form:"ipaddress" binding:"required"`
	Port      string `form:"port"  binding:"required"`
}
