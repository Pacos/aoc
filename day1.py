def parse_data(filename):
    with open(filename) as f:
        return [line.rstrip() for line in f]


def compute(lines):
    nbs = []
    for line in lines:
        digits = [c for c in line if c.isdigit()]
        if len(digits) > 0:
            nbs.append(int(digits[0] + digits[-1]))
    return sum(nbs)


def translate_numbers(lines):
    digits = {
        "oneight": "18",
        "twone": "21",
        "threeight": "38",
        "fiveight": "58",
        "sevenine": "79",
        "eightwo": "82",
        "eighthree": "83",
        "nineight": "98",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9"
    }
    for word, digit in digits.items():
        lines = [line.replace(word, digit) for line in lines]
    return lines


if __name__ == "__main__":
    data = parse_data("data/day1")
    print("1a >")
    print(compute(data))
    print("1b >")
    print(compute(translate_numbers(data)))
