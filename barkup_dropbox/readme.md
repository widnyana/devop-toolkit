Barkup + Dropbox
================

# what is this?

a poor-man mysql backup utility, it will backup your mysql db and send its tar.gz to your dropbox

## How to

make sure you already set your `$GOPATH`, and your dropbox destination path are already exist.

1. `go get github.com/keighl/barkup`
2. cd to that directory (`$GOPATH/src/github.com/keighl/barkup`), and copy `dropbox.go` there
3. create new directory, mine called `cmd`, and put `main.go` inside.
4. change the configuration with yours, then you can `go run main.go` or `go build -o barkup main.go && ./barkup`


peace out :v: