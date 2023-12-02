import re
import math


def parse_data(filename):
    with open(filename) as f:
        lines = [line.rstrip() for line in f]
    games = {}
    for line in lines:
        game_match = re.search("Game \d*:\s", line)
        game = int(re.search("\d+", game_match.group(0)).group(0))
        drafts = []
        for s in re.split("; ", line[game_match.end():]):
            draft = {}
            for color in ["red", "green", "blue"]:
                match = re.search(f"(\d+) {color}", s)
                if match:
                    draft[color] = int(match.group(1))
                else:
                    draft[color] = 0
            drafts.append(draft)
        games[game] = drafts
    return games


def compute_a(games):
    bag = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }
    possible_games = []
    for game, drafts in games.items():
        possible = True
        for draft in drafts:
            for color, limit in bag.items():
                if draft[color] > limit:
                    possible = False
        if possible:
            possible_games.append(game)
    return sum(possible_games)


def compute_b(games):
    games_powers = []
    for game, drafts in games.items():
        color_max = {
            "red": 0,
            "green": 0,
            "blue": 0
        }
        for draft in drafts:
            for color, current_max in color_max.items():
                if draft[color] > current_max:
                    color_max[color] = draft[color]
        games_powers.append(math.prod(color_max.values()))
    return sum(games_powers)


if __name__ == "__main__":
    games = parse_data("data/day2")
    print("2a >")
    print(compute_a(games))
    print("2b >")
    print(compute_b(games))
