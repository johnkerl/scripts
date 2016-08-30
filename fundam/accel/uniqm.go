// Build instructions: go build uniqm.go

package main

import (
	"fmt"
	"log"
	"os"
	"bufio"
	"io"
)

// ----------------------------------------------------------------
func main() {
	args := os.Args[1:]

	ok := true
	if len(args) == 0 {
		ok = uniqm("-") && ok
	} else {
		for _, arg := range args {
			ok = uniqm(arg) && ok // ok && uniqm(arg): not called after error
		}
	}
	if ok {
		os.Exit(0)
	} else {
		os.Exit(1)
	}
}

// ----------------------------------------------------------------
func uniqm(sourceName string) (ok bool) {
	set := make(map[string]bool)
	sourceStream := os.Stdin
	if sourceName != "-" {
		var err error
		if sourceStream, err = os.Open(sourceName); err != nil {
			log.Println(err)
			return false
		}
	}

	reader := bufio.NewReader(sourceStream)
	eof := false

	for !eof {
		line, err := reader.ReadString('\n')
		if err == io.EOF {
			err = nil
			eof = true
		} else if err != nil {
			log.Println(err)
			if sourceName != "-" {
				sourceStream.Close()
			}
			return false
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
	if sourceName != "-" {
		sourceStream.Close()
	}

	return true
}
