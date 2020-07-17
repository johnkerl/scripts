// ================================================================
// Build instructions:
//   export GOPATH=${GOPATH}:$(pwd)
// or
//   export GOPATH=$(pwd)
// then
//   go build stamplines.go

// Example usage:
// stamplines -d repeat 100 ./foo
// stamplines repeat 100 ./foo

// Example test input data:
// $ cat foo
// #!/bin/bash
// r=$[RANDOM/50]
// millisleep $r
// echo $r
// ================================================================
package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"os"
	"os/exec"
	"strings"
	"time"

	"simpletimeformat"
)

func main() {
	doDeltas := false
	args := os.Args[1:]
	if len(os.Args) >= 2 && os.Args[1] == "-d" {
		doDeltas = true
		args = os.Args[2:]
	}

	ok := true
	if len(args) == 0 {
		ok = stampLinesFilter(os.Stdin, doDeltas)
	} else {
		pcmd := exec.Command("bash", "-c", strings.Join(args, " "))
		o, oerr := pcmd.StdoutPipe()
		if oerr != nil { log.Fatal(oerr) }
		serr := pcmd.Start()
		if serr != nil { log.Fatal(serr) }
		ok = stampLinesFilter(o, doDeltas)

		// E.g. "stamplines ls /no/such/path".
		// It's usually reasonable to wait for status now that the
		// subprocess has closed its stdout.
		werr := pcmd.Wait()
		if werr != nil {
			fmt.Println(werr)
			ok = false
		}
	}

	if ok {
		os.Exit(0)
	} else {
		os.Exit(1)
	}
}

// ----------------------------------------------------------------
func stampLinesFilter(sourceStream io.Reader, doDeltas bool) (ok bool) {
	reader := bufio.NewReader(sourceStream)
	eof := false

	t1 := time.Now().UnixNano()

	for !eof {
		line, err := reader.ReadString('\n')
		if err == io.EOF {
			err = nil
			eof = true
		} else if err != nil {
			log.Println(err)
			return false
		} else {
			if (doDeltas) {
				t2 := time.Now().UnixNano()
				deltaSec := float64(t2 - t1) * 1e-9
				fmt.Printf("%.9f  %s", deltaSec, line);
				t1 = t2
			} else {
				fmt.Printf("[%s] %s",
					simpletimeformat.YMDhmsnzStamp(time.Now()),
					line)
			}
		}
	}

	return true
}
