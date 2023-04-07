package models

import (
	"log"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

// DB is the he database connection.
var DB *gorm.DB

// SetupDatabase migrates and sets up the database.
func SetupDatabase(dbTarget string) {

	// Connect to the database.
	db, err := gorm.Open(sqlite.Open(dbTarget), &gorm.Config{})
	if err != nil {
		log.Fatalf("Failed to connect to database: %s", err)
	}

	// Migrate the schema
	migrerr := db.AutoMigrate(
		&Gateway{},
	)
	if migrerr != nil {
		log.Fatalf("Error migrating database: %s", err)
	}

	DB = db
}
