package main

func hashContent(items string) map[rune]int {
	var charCounter = map[rune]int{}
	for _, char := range items {
		charCounter[char]++
	}
	return charCounter
}

func findCommonItem(rucksack string) rune {
	compartimentSize := len(rucksack) / 2
	firstCompartimentItems := hashContent(rucksack[:compartimentSize])
	secondCompartimentItems := hashContent(rucksack[compartimentSize:])
	for char := range firstCompartimentItems {
		if _, found := secondCompartimentItems[char]; found {
			return char
		}
	}
	return '0'
}

func findCommonItem3Rucksacks(rucksacks []string) rune {
	itemsMap1 := hashContent(rucksacks[0])
	itemsMap2 := hashContent(rucksacks[1])
	itemsMap3 := hashContent(rucksacks[2])
	for char := range itemsMap1 {
		if _, foundIn2 := itemsMap2[char]; foundIn2 {
			if _, foundIn3 := itemsMap3[char]; foundIn3 {
				return char
			}
		}
	}
	return '0'
}

func getItemPriority(item rune) int {
	ascii := int(item)
	if (ascii >= 97 && ascii <= 123) {
		return ascii - 96
	} else if (ascii >= 65 && ascii <= 91) {
		return ascii  - 38
	}
	return 0
}


func computeDay3Part1(lines []string) int {
	var totalPriorities int
	for _, rucksack := range lines {
		item := findCommonItem(rucksack)
		totalPriorities += getItemPriority(item)
	}
	return totalPriorities
}

func computeDay3Part2(lines []string) int {
	var totalPriorities int
	var currentGroup []string
	for i := 0; i<len(lines); i++ {
		switch i%3 {
		case 0:
			currentGroup = []string{lines[i]}
		case 1:
			currentGroup = append(currentGroup, lines[i])
		case 2:
			currentGroup = append(currentGroup, lines[i])
			totalPriorities += getItemPriority(findCommonItem3Rucksacks(currentGroup))
		}
	}
	return totalPriorities
}
