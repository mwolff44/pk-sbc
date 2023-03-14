package main

import (
	"log"

	"pks.pyfreebilling.com/app"
)

func main() {
	log.Println("Starting PKS-admin server...")

	app.StartApp()
}
