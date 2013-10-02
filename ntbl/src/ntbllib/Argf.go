// ================================================================
// Return a line at a time from multiple file names. Related to Ruby's ARGF or
// Perl's "while ($line = <>)".
//
// * If file_names has length >= 1, returns one line at a time from the first
//   file name until all are consumed, then all from the second file name, etc.
//
// * If file_names has length 0, returns one line at a time from stdin until
//   all are consumed.
//
// John Kerl
// 2013-10-01
// ================================================================

package ntbllib

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"os"
	"strings"
)

// ================================================================
type Argf struct {
	file_names              []string

	current_file_name_index int
	current_handle          *os.File
	reader                  *bufio.Reader
	exhausted               bool
}

// ----------------------------------------------------------------
func NewArgf(file_names []string) *Argf {
	if len(file_names) == 0 {
		return &Argf{[]string{"-"}, -1, nil, nil, false}
	} else {
		return &Argf{file_names, -1, nil, nil, false}
	}
}

// ----------------------------------------------------------------
func (self Argf) Dump() {
	fmt.Printf("## #file_names = %d\n", len(self.file_names))
	for i, file_name := range self.file_names {
		fmt.Printf("## [%d] %s\n", i, file_name)
	}
	fmt.Printf("## current_index  = %d\n", self.current_file_name_index)
	fmt.Printf("## current_handle = %p\n", self.current_handle)
	fmt.Printf("## reader         = %p\n", self.reader)
}

// ----------------------------------------------------------------
// xxx stdin ...

func (self *Argf) ReadLine() (line string, err error) {
	if self.exhausted {
		return "", io.EOF
	}

	for {
		// xxx delegate to stdin-reader or filenames reader
		// xxx make a next-handle method ...
		// xxx make a next-filename method?
		if self.current_handle == nil {
			// acquire next file name
			self.current_file_name_index++
			if self.current_file_name_index >= len(self.file_names) {
				self.exhausted = true
				return "", io.EOF
			}

			// acquire handle and reader from file name
			current_file_name := self.file_names[self.current_file_name_index]
			if current_file_name == "-" {
				self.current_handle = os.Stdin
			} else {
				handle, open_err := os.Open(self.file_names[self.current_file_name_index])
				if open_err != nil {
					log.Fatal(open_err)
				}
				self.current_handle = handle
			}

			self.reader = bufio.NewReader(self.current_handle)
		}
		line, read_err := self.reader.ReadString('\n')
		if read_err == io.EOF {
			self.current_handle.Close()
			self.current_handle = nil
		} else {
			return strings.TrimRight(line, "\n"), nil
		}
	}
}
