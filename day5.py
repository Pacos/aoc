import re
from dataclasses import dataclass


@dataclass
class SeedRange:
    start: int
    end: int

    def includes(self, value):
        return self.start <= value <= self.end


@dataclass
class ConversionRange:
    source_start: int
    source_end: int
    offset: int
    destination_start: int

    def matches(self, value):
        if self.source_start <= value <= self.source_end:
            return value + self.offset
        return None

    def reverse_matches(self, value):
        if self.source_start <= value - self.offset <= self.source_end:
            return value - self.offset
        return None


@dataclass
class ConversionMap:
    id: int
    name: str
    ranges: list[ConversionRange]

    def lookup(self, value):
        for rng in self.ranges:
            if converted := rng.matches(value):
                return converted
        return value

    def reverse_lookup(self, value):
        #print(self)
        for rng in self.ranges:
            #print(rng)
            if converted := rng.reverse_matches(value):
                return converted
        return value


class Almanac:
    def __init__(self, filename):
        with open(filename) as f:
            lines = [line.rstrip() for line in f]
        self.maps = []
        self.seeds = []
        self.seeds_ranges = []
        current_map = None
        for line in lines:
            if line:
                if seed_line := re.match("seeds: (.*)", line):
                    self.seeds = [int(s) for s in re.split(" ", seed_line.group(1))]
                if map_line := re.match("(.+-to-.+) map:", line):
                    current_map = ConversionMap(len(self.maps), map_line.group(1), [])
                if range_line := re.match("[0-9\s]+", line):
                    range_numbers = re.split(" ", range_line.group(0))
                    current_map.ranges.append(ConversionRange(
                        int(range_numbers[1]),
                        int(range_numbers[1]) + int(range_numbers[2]) - 1,
                        int(range_numbers[0]) - int(range_numbers[1]),
                        int(range_numbers[0])
                    ))
            else:
                if current_map:
                    self.maps.append(current_map)
                    current_map = None
        self.maps.append(current_map)
        for i in range(int(len(self.seeds)/2)):
            self.seeds_ranges.append(SeedRange(
                self.seeds[i*2],
                self.seeds[i*2] + self.seeds[i*2+1]
            ))
        self.seed_ranges_ceiling = max([seed_range.end for seed_range in self.seeds_ranges])
        self.seed_ranges_floor = min([seed_range.start for seed_range in self.seeds_ranges])

    def convert_seed_to_location(self, seed):
        for mp in self.maps:
            seed = mp.lookup(seed)
        return seed

    def convert_location_to_seed(self, location):
        for mp in self.maps[::-1]:
            location = mp.reverse_lookup(location)
        return location

    def find_best_location(self):
        return min([self.convert_seed_to_location(seed) for seed in self.seeds])

    def find_best_location_for_seed_ranges(self):
        for i in range(0, 10000000000):
            for rng in self.seeds_ranges:
                if rng.includes(self.convert_location_to_seed(i)):
                    return i


if __name__ == "__main__":
    test_almanac = Almanac("data/day5-sample")
    assert test_almanac.find_best_location() == 35
    assert test_almanac.find_best_location_for_seed_ranges() == 46

    almanac = Almanac("data/day5")
    print("5a >")
    print(almanac.find_best_location())
    print("5b >")
    print(almanac.find_best_location_for_seed_ranges())
