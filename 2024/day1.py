from collections import Counter

def parse_data(filename):
    with open(filename) as f:
        lefts = []
        rights = []
        for line in f:
            elems = line.rstrip().split("   ")
            lefts.append(int(elems[0]))
            rights.append(int(elems[1]))
    return lefts, rights

def compute_a(lefts, rights):
    lefts = sorted(lefts)
    rights = sorted(rights)
    return sum([abs(lefts[i] - rights[i]) for i in range(len(lefts))])

def compute_b(lefts, rights):
    r_occ = Counter(rights)
    return sum([item * r_occ[item] for item in lefts])

if __name__ == "__main__":
    lefts, rights = parse_data("data/day1")
    print(f"Day 1a > {compute_a(lefts, rights)}")
    print(f"Day 1b > {compute_b(lefts, rights)}")

