from dataclasses import dataclass
import time

from pyfiglet import Figlet
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

@dataclass
class Direction:
    h_offset: int
    v_offset: int

    def __repr__(self):
        return f"Dir @ h: {self.h_offset} - v: {self.v_offset}"


class Char:
    def __init__(self, text: str, line: int, col: int):
        self.text: str = text
        self.line: int = line
        self.col: int = col
        self.is_processed: bool = False
        self.is_xmas: bool = False

    def get_as_markup(self) -> Text:
        if self.is_xmas:
            return Text.from_markup(f"[blink green]{self.text}[blink green]")
        if self.is_processed:
            return Text.from_markup(f"[bright_black]{self.text}[bright_black]")
        return Text(self.text)

    def __repr__(self):
        return f"Char @ text: {self.text} - line: {self.line} - col: {self.col}"


class Grid:
    def __init__(self, filepath):
        with open(filepath) as f:
            lines = [[Char(text=char, line=l_idx, col=c_idx) for c_idx, char in enumerate(line.strip())] for l_idx, line in
                     enumerate(f)]
        self.lines: list[list[Char]] = lines
        self.height: int = len(self.lines)
        self.width: int = len(self.lines[0])
        self.nb_xmas: int = 0

    def get_as_markup(self) -> Text:
        text = Text()
        for line in self.lines:
            for char in line:
                text.append_text(char.get_as_markup())
            text.append("\n")
        return text

    def _get_search_directions_xmas(self, char: Char) -> list[Direction]:
        search_directions = {
            "east": Direction(h_offset=1, v_offset=0),
            "south_east": Direction(h_offset=1, v_offset=1),
            "south": Direction(h_offset=0, v_offset=1),
            "south_west": Direction(h_offset=-1, v_offset=1),
            "west": Direction(h_offset=-1, v_offset=0),
            "north_west": Direction(h_offset=-1, v_offset=-1),
            "north": Direction(h_offset=0, v_offset=-1),
            "north_east": Direction(h_offset=1, v_offset=-1),
        }
        if char.line < 3:
            search_directions.pop("north", None)
            search_directions.pop("north_east", None)
            search_directions.pop("north_west", None)
        if char.line > self.height - 4:
            search_directions.pop("south", None)
            search_directions.pop("south_east", None)
            search_directions.pop("south_west", None)
        if char.col < 3:
            search_directions.pop("west", None)
            search_directions.pop("south_west", None)
            search_directions.pop("north_west", None)
        if char.col > self.width - 4:
            search_directions.pop("east", None)
            search_directions.pop("south_east", None)
            search_directions.pop("north_east", None)
        return [dir for dir in search_directions.values()]

    def _check_direction_xmas(self, start: Char, dir: Direction):
        return "".join([self.lines[start.line + i*dir.v_offset][start.col + i*dir.h_offset].text for i in range(4)]) == "XMAS"


    def search_position_for_xmas(self, start: Char) -> None:
        if start.text != "X":
            start.is_processed = True
            return
        dirs: list[Direction] = self._get_search_directions_xmas(start)
        for dir in dirs:
            if "".join([self.lines[start.line + i*dir.v_offset][start.col + i*dir.h_offset].text for i in range(4)]) == "XMAS":
                self.nb_xmas += 1
                for i in range(4):
                    self.lines[start.line + i*dir.v_offset][start.col + i*dir.h_offset].is_xmas = True

        if not start.is_xmas:
            start.is_processed = True

    def search_for_xmas(self) -> None:
        for line in self.lines:
            for char in line:
                self.search_position_for_xmas(char)


if __name__ == "__main__":
    grid: Grid = Grid("data/day4")

    console = Console()
    console.clear()

    with console.screen() as screen:
        screen.update(Panel(grid.get_as_markup()))
        time.sleep(0.1)
        for idx, line in enumerate(grid.lines):
            for char in line:
                grid.search_position_for_xmas(char)
            time.sleep(0.01)
            if idx % 10 == 0:
                screen.update(Panel(grid.get_as_markup()))
        screen.update(Panel(grid.get_as_markup()))
        time.sleep(3)

        result = Figlet(font="starwars").renderText(f"Number of XMAS:\n{grid.nb_xmas}")
        screen.update(Panel(result))

        time.sleep(3)
