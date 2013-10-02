package main
import (
	"fmt"
	"os"
	"io"
	"ntbllib"
	"log"
)

// ----------------------------------------------------------------
func main() {
	argf := ntbllib.NewArgf(os.Args[1:])
	var s string
	var e error

//	//argf.Dump()
//	for i := 0; i < 20; i++ {
//		s, e = argf.ReadLine()
//		if e == nil {
//			fmt.Printf("LINE: >>%s<<\n", s)
//		} else {
//			fmt.Printf("e=>>%s<<\n", e.Error())
//		}
//		//argf.Dump()
//	}

	for {
		s, e = argf.ReadLine()
		if e == io.EOF {
			break
		} else if e != nil{
			log.Fatal(e)
		}
		fmt.Println(s)
	}
}
