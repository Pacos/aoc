from dataclasses import dataclass
from itertools import chain
import re

from loguru import logger

from tools.observability import monitor_exec_time


def parse_data(filename):
    with open(filename) as f:
        return f.read().replace("\n", "")


@dataclass
class Mul:
    left: int
    right: int

    def op(self):
        return self.left * self.right


def find_muls(memory):
    return [
        Mul(left=int(mul[0]), right=int(mul[1]))
        for mul in re.findall(r"mul\((\d+),(\d+)\)", memory)
    ]


def find_muls_with_intervals(memory):
    intervals = []
    prev_do = True
    cur_interval = {"start": 0, "end": None}
    for match in re.finditer(r"do(n't)?\(\)", memory):
        if match.group(0) == "do()" and not prev_do:
            cur_interval["start"] = match.end()
            prev_do = True
        if match.group(0) == "don't()" and prev_do:
            cur_interval["end"] = match.start()
            intervals.append(cur_interval)
            cur_interval = {"start": match.end(), "end": None}
            prev_do = False
    if cur_interval["end"] is None:
        cur_interval["end"] = len(memory)
        intervals.append(cur_interval)

    return list(
        chain.from_iterable(
            [
                find_muls(memory[interval["start"] : interval["end"]])
                for interval in intervals
            ]
        )
    )


@monitor_exec_time
def compute_a(memory):
    return sum([mul.op() for mul in find_muls(memory)])


@monitor_exec_time
def compute_b(memory):
    return sum([mul.op() for mul in find_muls_with_intervals(memory)])


if __name__ == "__main__":
    memory = parse_data("data/day3")

    memory_sample_a = parse_data("data/day3a-sample")
    assert compute_a(memory_sample_a) == 161

    memory_sample_b = parse_data("data/day3b-sample")
    assert compute_b(memory_sample_b) == 48

    logger.info(f"Day 3a > {compute_a(memory)}")
    logger.info(f"Day 3b > {compute_b(memory)}")
