package main

// Prints n basenames, e.g. if the pwd is /a/b/c/d/e/f then:
//
// n output
// - ------
// 1 f
// 2 e/f
// 3 d/e/f
// 4 c/d/e/f
// 5 b/c/d/e/f
// 6 /a/b/c/d/e/f

import (
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

func nth_basenames(path string, n int) string {
	basenames := make([]string, 0)

	for i := 0; i < n; i++ {
		dir := filepath.Dir(path)
		base := filepath.Base(path)
		basenames = append([]string{base}, basenames...)
		if dir == "/" {
			basenames = append([]string{""}, basenames...)
			break
		}
		path = dir
	}
	retval := strings.Join(basenames, "/")
	if retval == "//" {
		return "/"
	} else {
		return retval
	}
}

func main() {
	n := 2
	if len(os.Args) == 2 {
		ntry, err := strconv.Atoi(os.Args[1])
		if err != nil {
			fmt.Fprintf(os.Stderr, "%s: cannot scan \"%s\" as integer.\n",
				os.Args[0], os.Args[1])
			return
		}
		n = ntry
	}

	pwd, err := os.Getwd()
	if err != nil {
		fmt.Println("Error getting current working directory:", err)
		return
	}
	basenames := nth_basenames(pwd, n)
	fmt.Println(basenames)
}
