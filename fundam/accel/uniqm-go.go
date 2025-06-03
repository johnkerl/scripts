/*
Build instructions: see Makefile
*/

package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

func main() {
	//argc := len(os.Args)
	//for argi := 0; argi < argc; argi++ {
	//}

	reader := bufio.NewReader(os.Stdin)
	uniqueLines := make(map[string]bool)

	for {
		line, err := reader.ReadString('\n')
		if err == io.EOF {
			break
		}
		if err != nil {
			os.Exit(1)
		}
		if line == "" {
			break
		}
		_, ok := uniqueLines[line]
		if !ok {
			fmt.Print(line)
			uniqueLines[line] = true
		}
	}
}
