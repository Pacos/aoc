package main

import (
	"sort"
	"strconv"
)

func computeDay1Part1(lines []string) int {

	var currentCaloriesByElf int = 0
	var maxCaloriesByElf int = 0

	for _, line := range lines {
		if line == "" {
			if currentCaloriesByElf > maxCaloriesByElf {
				maxCaloriesByElf = currentCaloriesByElf
			}
			currentCaloriesByElf = 0

		} else {
			calories, _ := strconv.Atoi(line)
			currentCaloriesByElf += calories
		}
	}

	return maxCaloriesByElf

}

func computeDay1Part2(lines []string) int {

	topThreeElvesCalories := []int{0}
	var currentCaloriesByElf int = 0
	var sumTopThreeElvesCalories int = 0

	for _, line := range lines {
		if line == "" {
			if currentCaloriesByElf > topThreeElvesCalories[0] {
				topThreeElvesCalories = append(topThreeElvesCalories, currentCaloriesByElf)
				if len(topThreeElvesCalories) > 3 {
					sort.Ints(topThreeElvesCalories)
					topThreeElvesCalories = topThreeElvesCalories[1:4]
				}
			}
			currentCaloriesByElf = 0

		} else {
			calories, _ := strconv.Atoi(line)
			currentCaloriesByElf += calories
		}
	}

	for i := 0; i < len(topThreeElvesCalories); i++ {
		sumTopThreeElvesCalories += topThreeElvesCalories[i]
	}

	return sumTopThreeElvesCalories

}