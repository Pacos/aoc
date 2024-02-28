package main

import (
	"bufio"
	"os"
)

func readLines(path string, addLastBlankLine bool) []string {
	file, _ := os.Open(path)
	defer file.Close()

	var lines []string

	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	if lines[len(lines)-1] != "" && addLastBlankLine {
		lines = append(lines, "")
	}

	return lines
}