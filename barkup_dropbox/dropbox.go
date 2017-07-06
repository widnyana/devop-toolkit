package barkup

import (
	"os"

	dropbox "github.com/tj/go-dropbox"
	dropy "github.com/tj/go-dropy"
)

// Dropbox is a `Storer` interface that puts an ExportResult to the specified Dropbox folder.
type Dropbox struct {
	// AccessToken your dropbox application key
	AccessToken string
}

// Store puts an `ExportResult` struct to an DropboxFolder within the specified directory
func (d *Dropbox) Store(result *ExportResult, destination string) *Error {

	if result.Error != nil {
		return result.Error
	}

	file, err := os.Open(result.Path)
	if err != nil {
		return makeErr(err, "")
	}
	defer file.Close()

	client := dropy.New(dropbox.New(dropbox.NewConfig(d.AccessToken)))
	err = client.Upload(destination, file)
	if err != nil {
		return makeErr(err, "")
	}
	return makeErr(nil, "")
}
