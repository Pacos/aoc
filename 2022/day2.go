package main

import (
	"strings"
)

func getRoundScore(opponent string, you string) int {
	var score int
	switch opponent {
	case "A":
		switch you {
		case "X":
			score = 1 + 3
		case "Y":
			score = 2 + 6
		case "Z":
			score = 3 + 0
		}
	case "B":
		switch you {
		case "X":
			score = 1 + 0
		case "Y":
			score = 2 + 3
		case "Z":
			score = 3 + 6
		}
	case "C":
		switch you {
		case "X":
			score = 1 + 6
		case "Y":
			score = 2 + 0
		case "Z":
			score = 3 + 3
		}
	}
	return score
}

func getStrategicShape(opponent string, roundResult string) string {
	var strategicShape string
	switch opponent {
	case "A":
		switch roundResult {
		case "X":
			strategicShape = "Z"
		case "Y":
			strategicShape = "X"
		case "Z":
			strategicShape = "Y"
		}
	case "B":
		switch roundResult {
		case "X":
			strategicShape = "X"
		case "Y":
			strategicShape = "Y"
		case "Z":
			strategicShape = "Z"
		}
	case "C":
		switch roundResult {
		case "X":
			strategicShape = "Y"
		case "Y":
			strategicShape = "Z"
		case "Z":
			strategicShape = "X"
		}
	}
	return strategicShape
}

func computeDay2Part1(lines []string) int {
	var totalScore int

	for _, round := range lines {
		totalScore += getRoundScore(strings.Split(round, " ")[0], strings.Split(round, " ")[1])
	}

	return totalScore
}

func computeDay2Part2(lines []string) int {
	var totalScore int
	var opponent, roundResult string
	for _, round := range lines {
		opponent = strings.Split(round, " ")[0]
		roundResult = strings.Split(round, " ")[1]
		totalScore += getRoundScore(opponent, getStrategicShape(opponent, roundResult))
	}

	return totalScore
}
