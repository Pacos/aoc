package main

import (
	"flag"
	"fmt"
)

func main() {

	day := flag.String("day", "day1", "day to compute")
	path := flag.String("path", "/data/day1-example", "path to source data")

	flag.Parse()

	switch *day {
	case "day1":
		lines := readLines(*path, true)
		fmt.Printf("part1 : %d\n", computeDay1Part1(lines))
		fmt.Printf("part2 : %d\n", computeDay1Part2(lines))
	case "day2":
		lines := readLines(*path, false)
		fmt.Printf("part1 : %d\n", computeDay2Part1(lines))
		fmt.Printf("part2 : %d\n", computeDay2Part2(lines))
	case "day3":
		lines := readLines(*path, false)
		fmt.Printf("part1 : %d\n", computeDay3Part1(lines))
		fmt.Printf("part2 : %d\n", computeDay3Part2(lines))
	default:
		fmt.Println("Error unknown day:", day)
		return
	}

}
