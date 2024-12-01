from collections import Counter

from loguru import logger

from tools.observability import monitor_exec_time

def parse_data(filename):
    with open(filename) as f:
        lefts = []
        rights = []
        for line in f:
            elems = line.rstrip().split("   ")
            lefts.append(int(elems[0]))
            rights.append(int(elems[1]))
    return lefts, rights

@monitor_exec_time
def compute_a(lefts, rights):
    lefts = sorted(lefts)
    rights = sorted(rights)
    return sum([abs(lefts[i] - rights[i]) for i in range(len(lefts))])

@monitor_exec_time
def compute_b(lefts, rights):
    r_occ = Counter(rights)
    return sum([item * r_occ[item] for item in lefts])

if __name__ == "__main__":
    lefts, rights = parse_data("data/day1")
    logger.info(f"Day 1a > {compute_a(lefts, rights)}")
    logger.info(f"Day 1b > {compute_b(lefts, rights)}")

