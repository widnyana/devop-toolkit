package main

import (
	"fmt"
	"time"

	"github.com/keighl/barkup"
)

func log(msg string) {
	t := time.Now()
	fmt.Printf("[%s] %s\n", t.Format(time.RFC3339), msg)
}

func main() {
	var (
		accessToken = "get your random string here: https://www.dropbox.com/developers/apps"
		location    = "/path/to/your/destination/on/dropbox"
	)
	t := time.Now()
	destination := fmt.Sprintf("%s/%d-%02d-%02d.tar.gz",
		location,
		t.Year(), t.Month(), t.Day(),
	)

	log("Starting backup.")
	mysql := &barkup.MySQL{
		Host:     "localhost",
		Port:     "3306",
		DB:       "database",
		User:     "root",
		Password: "secret",
	}

	dbx := &barkup.Dropbox{
		AccessToken: accessToken,
	}

	backup := mysql.Export()
	log(fmt.Sprintf("sending backup of %s to dropbox. source: %s, destination: %s",
		mysql.DB, backup.Path, destination))

	err := backup.To(destination, dbx)
	if err != nil {
		log(err.Error())
	} else {
		log("Done!")
	}

}
