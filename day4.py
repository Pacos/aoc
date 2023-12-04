import re
import math


class Scratchcards:
    def __init__(self, filename):
        with open(filename) as f:
            lines = [line.rstrip() for line in f]
        self.cards = []
        for idx, line in enumerate(lines):
            line = re.sub("Card\s+\d+:\s", "", line)
            numbers = re.split("\|", line)
            winning_numbers = [n for n in re.split("\s+", numbers[0]) if n]
            drawn_numbers = [n for n in re.split("\s+", numbers[1]) if n]
            self.cards.append({
                "id": idx+1,
                "winners": winning_numbers,
                "drawn": drawn_numbers,
                "copies": 1
            })

    @staticmethod
    def get_card_matches(card):
        return len(list(set(card["winners"]) & set(card["drawn"])))

    def get_points(self):
        points = []
        for card in self.cards:
            matches = self.get_card_matches(card)
            if matches == 0:
                points.append(0)
            else:
                points.append(int(math.pow(2, matches - 1)))
        return sum(points)

    def get_copied_scratchcards(self):
        for idx, card in enumerate(self.cards):
            for i in range(1, self.get_card_matches(card)+1):
                self.cards[idx+i]["copies"] += card["copies"]
        return sum([card["copies"] for card in self.cards])


if __name__ == "__main__":
    scratches = Scratchcards("data/day4")
    print("4a >")
    print(scratches.get_points())
    print("4b >")
    print(scratches.get_copied_scratchcards())
