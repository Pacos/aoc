import re
import math
from dataclasses import dataclass


@dataclass
class Race:
    time: int
    distance_to_beat: int

    def get_min_hold_time(self):
        return int((self.time - math.sqrt(self.time*self.time - 4*self.distance_to_beat))/2)+1

    def get_max_hold_time(self):
        root = (self.time + math.sqrt(self.time*self.time - 4*self.distance_to_beat))/2
        if root == int(root):
            return int(root)-1
        return int(root)

    def count_valid_hold_times(self):
        return self.get_max_hold_time() - self.get_min_hold_time() + 1


class Competition:
    def __init__(self, filename, part):
        with open(filename) as f:
            lines = [line.rstrip() for line in f]
        self.races = []
        if part == 1:
            times = []
            distances = []
            for line in lines:
                if time_line := re.match("Time:(.*)", line):
                    times = [int(t.strip()) for t in re.split(" ", time_line.group(1).strip()) if t.strip()]
                if distance_line := re.match("Distance:(.*)", line):
                    distances = [int(d.strip()) for d in re.split(" ", distance_line.group(1).strip()) if d.strip()]
            for idx, time in enumerate(times):
                self.races.append(Race(time, distances[idx]))
        else:
            time = 0
            distance = 0
            for line in lines:
                if time_line := re.match("Time:(.*)", line.replace(" ", "")):
                    time = int(time_line.group(1))
                if distance_line := re.match("Distance:(.*)", line.replace(" ", "")):
                    distance = int(distance_line.group(1))
            self.races.append(Race(time, distance))

    def get_product_count_valid_hold_times(self):
        return math.prod([race.count_valid_hold_times() for race in self.races])


if __name__ == "__main__":
    test_comp_a = Competition("data/day6-sample", 1)
    assert test_comp_a.get_product_count_valid_hold_times() == 288
    test_comp_b = Competition("data/day6-sample", 2)
    assert test_comp_b.get_product_count_valid_hold_times() == 71503
    comp_a = Competition("data/day6", 1)
    comp_b = Competition("data/day6", 2)
    print("6a >")
    print(comp_a.get_product_count_valid_hold_times())
    print("6b >")
    print(comp_b.get_product_count_valid_hold_times())
