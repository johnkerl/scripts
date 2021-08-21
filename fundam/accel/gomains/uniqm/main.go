// Build instructions:
// export GOPATH=$(pwd)
// go build uniqm.go

package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"os"

	"github.com/johnkerl/scripts/fundam/accel/golib/argf"
)

// ----------------------------------------------------------------
func main() {
	args := os.Args[1:]

	istream, err := argf.Open(args)
	if err != nil {
		log.Println(err)
		os.Exit(1)
	}

	err = uniqm(istream)

	if err != nil {
		log.Println(err)
		os.Exit(1)
	} else {
		os.Exit(0)
	}
}

// ----------------------------------------------------------------
func uniqm(istream io.Reader) error {
	set := make(map[string]bool)
	reader := bufio.NewReader(istream)
	eof := false

	for !eof {
		line, err := reader.ReadString('\n')
		if err == io.EOF {
			err = nil
			eof = true
		} else if err != nil {
			return err
		} else {
			// This is how to do a chomp:
			//line = strings.TrimRight(line, "\n")
			if set[line] {
			} else {
				fmt.Print(line)
				set[line] = true
			}
		}
	}

	return nil
}
