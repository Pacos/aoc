import re
import math


class Engine:
    def __init__(self, filename):
        with open(filename) as f:
            lines = [line.rstrip() for line in f]
        self.parts = []
        self.symbols = []
        self.gears = []
        self.nb_lines = 0
        for line in lines:
            self.nb_lines += 1
            line_parts = []
            line_symbols = []
            line_gears = []
            for nb in re.finditer(r"\d+", line):
                line_parts.append({
                    "value": int(nb.group(0)),
                    "start": nb.start(),
                    "end": nb.end()
                })
            for sym in re.finditer(r"[^0-9.]", line):
                line_symbols.append({
                    "symbol": sym.group(0),
                    "position": sym.start()
                })
            for gear in re.finditer(r"[*]", line):
                line_gears.append(gear.start())
            self.parts.append(line_parts)
            self.symbols.append(line_symbols)
            self.gears.append(line_gears)

    def get_part_numbers(self):
        matched_parts = []
        for line, parts_line in enumerate(self.parts):
            for part in parts_line:
                matched = False
                for sym_line in range(max(0, line - 1), min(self.nb_lines - 1, line + 1) + 1):
                    if not matched:
                        for symbol in self.symbols[sym_line]:
                            if part["start"] - 1 <= symbol["position"] <= part["end"]:
                                matched = True
                                break
                if matched:
                    matched_parts.append(part["value"])
        return sum(matched_parts)

    def get_gear_ratios(self):
        gear_ratios = []
        for line, gears in enumerate(self.gears):
            for gear in gears:
                matched_parts = []
                for part_line in range(max(0, line - 1), min(self.nb_lines - 1, line + 1) + 1):
                    for part in self.parts[part_line]:
                        if part["start"] - 1 <= gear <= part["end"]:
                            matched_parts.append(part["value"])
                if len(matched_parts) == 2:
                    gear_ratios.append(math.prod(matched_parts))
        return sum(gear_ratios)


if __name__ == "__main__":
    engine = Engine("data/day3")
    print("3a >")
    print(engine.get_part_numbers())
    print("3b >")
    print(engine.get_gear_ratios())
