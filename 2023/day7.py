import re
from itertools import groupby


CARD_ORDER = {
    "A": "m",
    "K": "l",
    "Q": "k",
    "J": "j",
    "T": "i",
    "9": "h",
    "8": "g",
    "7": "f",
    "6": "e",
    "5": "d",
    "4": "c",
    "3": "b",
    "2": "a",
}

CARD_ORDER_JOKER = {
    "A": "m",
    "K": "l",
    "Q": "k",
    "T": "j",
    "9": "i",
    "8": "h",
    "7": "g",
    "6": "f",
    "5": "e",
    "4": "d",
    "3": "c",
    "2": "b",
    "J": "a",
}

TYPE_ORDER = {
    "5K": 7,
    "4K": 6,
    "FH": 5,
    "3K": 4,
    "2P": 3,
    "1P": 2,
    "H": 1
}


class Hand:
    def __init__(self, cards, bet, joker=False):
        self.cards = cards
        self.bet = int(bet)
        if joker:
            self.type = self.get_type_with_joker(cards)
            self.cards_hash = "".join([CARD_ORDER_JOKER[card] for card in self.cards])
        else:
            self.type = self.get_type_without_joker(cards)
            self.cards_hash = "".join([CARD_ORDER[card] for card in self.cards])

    def __eq__(self, other):
        return self.cards == other.cards

    def __lt__(self, other):
        if self.type != other.type:
            return TYPE_ORDER[self.type] < TYPE_ORDER[other.type]
        return self.cards_hash < other.cards_hash

    def __repr__(self):
        return f"<{self.cards} - {self.type} - {self.bet} - {self.cards_hash}>"

    @staticmethod
    def get_type_from_occurrences(occurrences):
        match occurrences:
            case [1, 1, 1, 1, 1]:
                return "H"
            case [1, 1, 1, 2]:
                return "1P"
            case [1, 2, 2]:
                return "2P"
            case [1, 1, 3]:
                return "3K"
            case [2, 3]:
                return "FH"
            case [1, 4]:
                return "4K"
            case [5]:
                return "5K"

    @staticmethod
    def get_type_without_joker(cards):
        occurrences = sorted([len(list(group)) for key, group in groupby(sorted(cards))])
        return Hand.get_type_from_occurrences(occurrences)

    @staticmethod
    def get_type_with_joker(cards):
        occurrences = [{"card": key, "occ": len(list(group))} for key, group in groupby(sorted(cards))]
        occurrences.sort(key=lambda x: x["occ"], reverse=True)
        if joker_occ := next((card for card in occurrences if card["card"] == "J"), None):
            occurrences.remove(joker_occ)
            if occurrences:
                occurrences[0]["occ"] += joker_occ["occ"]
            else:
                return "5K"
        return Hand.get_type_from_occurrences(sorted([card["occ"] for card in occurrences]))


class Game:
    def __init__(self, filename):
        with open(filename) as f:
            lines = [line.rstrip() for line in f]
        self.hands = []
        self.joker_hands = []
        for line in lines:
            elems = re.split(" ", line)
            self.hands.append(Hand(cards=elems[0], bet=elems[1]))
            self.joker_hands.append(Hand(cards=elems[0], bet=elems[1], joker=True))
        self.hands.sort()
        self.joker_hands.sort()

    def get_total_winnings(self):
        return sum([(idx+1)*hand.bet for idx, hand in enumerate(self.hands)])

    def get_total_winnings_with_jokers(self):
        return sum([(idx+1)*hand.bet for idx, hand in enumerate(self.joker_hands)])


if __name__ == "__main__":
    test_game = Game("data/day7-sample")
    assert test_game.get_total_winnings() == 6440
    assert test_game.get_total_winnings_with_jokers() == 5905

    game = Game("data/day7")
    print("7a >")
    print(game.get_total_winnings())
    print("7b >")
    print(game.get_total_winnings_with_jokers())

