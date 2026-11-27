package main

import "fmt"

func ActivePodForUTC(hour int) string {
	if hour >= 13 && hour < 21 {
		return "AMER-NEW-YORK"
	}
	if hour >= 5 && hour < 13 {
		return "EMEA-FRANKFURT"
	}
	return "APAC-SINGAPORE"
}

func main() {
	fmt.Printf("FTS Go Solar Dispatcher | 02:00 UTC -> %s | 09:00 UTC -> %s | 16:00 UTC -> %s\n",
		ActivePodForUTC(2), ActivePodForUTC(9), ActivePodForUTC(16))
}
