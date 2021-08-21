package simpletimeformat

import (
	"fmt"
	"time"
)

func YMDhmsnzStamp(t time.Time) string {
	YYYY := t.Year()
	MM := int(t.Month())
	DD := t.Day()
	hh := t.Hour()
	mm := t.Minute()
	ss := t.Second()
	nnn := t.Nanosecond()

	_, offSecs := t.Zone()

	offSign := "+"
	absOffHrMin := offSecs
	if offSecs < 0 {
		offSign = "-"
		absOffHrMin = -absOffHrMin
	}
	absOffHrMin /= 60
	return fmt.Sprintf(
		"%04d%02d%02d %02d:%02d:%02d.%09d %s%02d%02d",
		YYYY, MM, DD, hh, mm, ss, nnn, offSign,
		absOffHrMin/60, absOffHrMin%60)
}
