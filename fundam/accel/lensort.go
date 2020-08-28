// Build instructions:
// export GOPATH=$(pwd)
// go build lensort
//
// Sorts lines by length.
// Compiled accelerator for ../lensort.

package main

import (
	"argf"
	"bufio"
	"container/list"
	"flag"
	"fmt"
	"io"
	"log"
	"os"
	"sort"
	"strings"
)

// ----------------------------------------------------------------
func usage() {
	fmt.Fprintf(os.Stderr, "Usage: %s [options] {filenames ...}\n", os.Args[0])
	fmt.Fprintf(os.Stderr, "If no file name is given, or if filename is \"-\", stdin is used.\n", os.Args[0])
	flag.PrintDefaults()
	os.Exit(1)
}

// ----------------------------------------------------------------
func main() {
	pDoReverse := flag.Bool("r", false, "Reverse sort (longest first)")

	flag.Usage = usage
	flag.Parse()
	doReverse := *pDoReverse

	args := flag.Args()

	istream, err := argf.Open(args)
	if err != nil {
		log.Println(err)
		os.Exit(1)
	}

	err = lensort(istream, doReverse)

	if err != nil {
		log.Println(err)
		os.Exit(1)
	} else {
		os.Exit(0)
	}
}

// ----------------------------------------------------------------
type lineAndLength struct {
	line   string
	length int
}

func lensort(istream io.Reader, doReverse bool) error {
	lines := list.New()
	numLines := 0

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
			line = strings.TrimRight(line, "\n")
			lines.PushBack(line)
			numLines++
		}
	}

	// Make an array of (string, strlen) pairs
	linesAndLengths := make([]lineAndLength, numLines)
	i := 0
	for iter := lines.Front(); iter != nil; iter = iter.Next() {
		line := iter.Value.(string)
		linesAndLengths[i].line = line
		linesAndLengths[i].length = len(line)
		i++
	}

	// Sort them
	if doReverse {
		sort.Slice(linesAndLengths, func(i, j int) bool {
			if linesAndLengths[i].length == linesAndLengths[j].length {
				return linesAndLengths[i].line > linesAndLengths[j].line
			} else {
				return linesAndLengths[i].length > linesAndLengths[j].length
			}
		})
	} else {
		sort.Slice(linesAndLengths, func(i, j int) bool {
			if linesAndLengths[i].length == linesAndLengths[j].length {
				return linesAndLengths[i].line < linesAndLengths[j].line
			} else {
				return linesAndLengths[i].length < linesAndLengths[j].length
			}
		})
	}

	// Print the lines only
	for i = 0; i < numLines; i++ {
		fmt.Println(linesAndLengths[i].line)
	}

	return nil
}
