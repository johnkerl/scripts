// Build instructions: go build hex.go

package main

import (
	"flag"
	"fmt"
	"os"
	"io"
	"log"
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
	pDoRaw := flag.Bool("r", false, "Count lines")

	flag.Usage = usage
	flag.Parse()
	args := flag.Args()

	doRaw := *pDoRaw

	ok := true
	if len(args) == 0 {
		ok = hexDump("-", doRaw) && ok
	} else {
		for _, arg := range args {
			ok = hexDump(arg, doRaw) && ok // ok && count(arg): not called after error
		}
	}
	if ok {
		os.Exit(0)
	} else {
		os.Exit(1)
	}
}

// ----------------------------------------------------------------
func hexDump(sourceName string, doRaw bool) (ok bool) {

	sourceStream := os.Stdin
	if sourceName != "-" {
		var err error
		if sourceStream, err = os.Open(sourceName); err != nil {
			log.Println(err)
			return false
		}
	}

	bytesPerClump := 4
	clumpsPerLine := 4
	bufferSize    := bytesPerClump * clumpsPerLine

	buffer := make([]byte, bufferSize)
	eof := false
	offset := 0

	for !eof {
		numBytesRead, err := sourceStream.Read(buffer)
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
			// Print offset "pre" part
			if (!doRaw) {
				fmt.Printf("%08x: ",  offset)
			}

			// Print hex payload
			for i := 0; i < bufferSize; i++ {
				if i < numBytesRead {
					fmt.Printf("%02x ", buffer[i])
				} else {
					fmt.Printf("   ")
				}
				if (i % bytesPerClump) == (bytesPerClump - 1) {
					if (i > 0) && (i < bufferSize-1) {
						fmt.Printf(" ")
					}
				}
			}

			// Print ASCII-dump "post" part
			if (!doRaw) {
				fmt.Printf("|")

				for i := 0; i < numBytesRead; i++ {
					if buffer[i] >= 0x20 &&  buffer[i] <= 0x7e {
						fmt.Printf("%c", buffer[i])
					} else {
						fmt.Printf(".")
					}
				}
				for i := numBytesRead; i < bufferSize; i++ {
					fmt.Print(" ")
				}
				fmt.Printf("|")
			}

			// Print line end
			fmt.Printf("\n")

			offset += numBytesRead
		}
	}

	if sourceName != "-" {
		sourceStream.Close()
	}

	return true
}
