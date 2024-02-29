package main

import (
	"regexp"
	"strconv"
)

type assignment struct {
	start int
	end   int
}

type assignmentPair struct {
	a1 assignment
	a2 assignment
}

func (aPair assignmentPair) assignmentsFullyContained() bool {
	return (aPair.a2.start >= aPair.a1.start && aPair.a2.end <= aPair.a1.end) || (aPair.a1.start >= aPair.a2.start && aPair.a1.end <= aPair.a2.end)
}

func (aPair assignmentPair) assignmentsOverlaps() bool {
	return aPair.a1.start <= aPair.a2.end && aPair.a1.end >= aPair.a2.start
}

func parseAssignments(lines []string) []assignmentPair {
	var a1, a2 assignment
	var ap assignmentPair
	aPairs := []assignmentPair{}
	re := regexp.MustCompile(`(\d+)-(\d+),(\d+)-(\d+)`)
	for _, line := range lines {
		matches := re.FindStringSubmatch(line)
		a1.start, _ = strconv.Atoi(matches[1])
		a1.end, _ = strconv.Atoi(matches[2])
		a2.start, _ = strconv.Atoi(matches[3])
		a2.end, _ = strconv.Atoi(matches[4])
		ap.a1 = a1
		ap.a2 = a2
		aPairs = append(aPairs, ap)
	}
	return aPairs
}

func computeDay4Part1(lines []string) int {
	var nbFullyContained int
	aPairs := parseAssignments(lines)
	for _, pair := range aPairs {
		if pair.assignmentsFullyContained() {
			nbFullyContained++
		}
	}
	return nbFullyContained
}

func computeDay4Part2(lines []string) int {
	var nbOverlaps int
	aPairs := parseAssignments(lines)
	for _, pair := range aPairs {
		if pair.assignmentsOverlaps() {
			nbOverlaps++
		}
	}
	return nbOverlaps
}
