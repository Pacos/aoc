from dataclasses import dataclass

from loguru import logger

from tools.observability import monitor_exec_time


@dataclass
class SearchDirections:
    east: bool = True
    south_east: bool = True
    south: bool = True
    south_west: bool = True
    west: bool = True
    north_west: bool = True
    north: bool = True
    north_east: bool = True


@dataclass
class Pos:
    line: int
    col: int


@dataclass
class Grid:
    lines: list[str]
    height: int
    width: int

    def _get_search_directions_xmas(self, pos: Pos) -> SearchDirections:
        dirs: SearchDirections = SearchDirections()
        if pos.line < 3:
            dirs.north = False
            dirs.north_east = False
            dirs.north_west = False
        if pos.line > self.height - 4:
            dirs.south = False
            dirs.south_east = False
            dirs.south_west = False
        if pos.col < 3:
            dirs.west = False
            dirs.south_west = False
            dirs.north_west = False
        if pos.col > self.width - 4:
            dirs.east = False
            dirs.south_east = False
            dirs.north_east = False
        return dirs

    def _search_position_for_xmas(self, pos: Pos) -> int:
        if self.lines[pos.line][pos.col] != "X":
            return 0
        dirs: SearchDirections = self._get_search_directions_xmas(pos)
        nb_xmas: int = 0
        if dirs.east and self.lines[pos.line][pos.col : pos.col + 4] == "XMAS":
            nb_xmas += 1
        if (
            dirs.south_east
            and "".join([self.lines[pos.line + i][pos.col + i] for i in range(4)])
            == "XMAS"
        ):
            nb_xmas += 1
        if (
            dirs.south
            and "".join([self.lines[pos.line + i][pos.col] for i in range(4)]) == "XMAS"
        ):
            nb_xmas += 1
        if (
            dirs.south_west
            and "".join([self.lines[pos.line + i][pos.col - i] for i in range(4)])
            == "XMAS"
        ):
            nb_xmas += 1
        if (
            dirs.west
            and self.lines[pos.line][pos.col - 3 : pos.col + 1][::-1] == "XMAS"
        ):
            nb_xmas += 1
        if (
            dirs.north_west
            and "".join([self.lines[pos.line - i][pos.col - i] for i in range(4)])
            == "XMAS"
        ):
            nb_xmas += 1
        if (
            dirs.north
            and "".join([self.lines[pos.line - i][pos.col] for i in range(4)]) == "XMAS"
        ):
            nb_xmas += 1
        if (
            dirs.north_east
            and "".join([self.lines[pos.line - i][pos.col + i] for i in range(4)])
            == "XMAS"
        ):
            nb_xmas += 1
        return nb_xmas

    def _is_cross_mas_searchable(self, pos: Pos) -> bool:
        if pos.col == 0:
            return False
        if pos.col == self.width - 1:
            return False
        if pos.line == 0:
            return False
        if pos.line == self.height - 1:
            return False
        return True

    def _search_position_for_cross_mas(self, pos: Pos) -> int:
        if self.lines[pos.line][pos.col] != "A":
            return 0
        if self._is_cross_mas_searchable(pos):
            if (
                (
                    self.lines[pos.line - 1][pos.col - 1] == "M"
                    and self.lines[pos.line + 1][pos.col + 1] == "S"
                )
                or (
                    self.lines[pos.line - 1][pos.col - 1] == "S"
                    and self.lines[pos.line + 1][pos.col + 1] == "M"
                )
            ) and (
                (
                    self.lines[pos.line + 1][pos.col - 1] == "M"
                    and self.lines[pos.line - 1][pos.col + 1] == "S"
                )
                or (
                    self.lines[pos.line + 1][pos.col - 1] == "S"
                    and self.lines[pos.line - 1][pos.col + 1] == "M"
                )
            ):
                return 1
        return 0

    @monitor_exec_time
    def search_for_xmas(self) -> int:
        total_xmas: int = 0
        for line in range(self.height):
            for col in range(self.width):
                if (nb_xmas := self._search_position_for_xmas(Pos(line, col))) > 0:
                    logger.debug(f"Position: {line},{col}: found {nb_xmas}")
                    total_xmas += nb_xmas

        return total_xmas

    @monitor_exec_time
    def search_for_cross_mas(self) -> int:
        total_cross_mas: int = 0
        for line in range(self.height):
            for col in range(self.width):
                if (nb_cross_mas := self._search_position_for_cross_mas(Pos(line, col))) > 0:
                    logger.debug(f"Position: {line},{col}: found {nb_cross_mas}")
                    total_cross_mas += nb_cross_mas

        return total_cross_mas


def parse_data(filename: str) -> Grid:
    with open(filename) as f:
        lines = [line.rstrip() for line in f]
    return Grid(lines=lines, height=len(lines), width=len(lines[0]))


def test_search_nb_xmas_in_grid():
    assert Grid(["XMAS", "....", "....", "...."], 4, 4).search_for_xmas() == 1
    assert Grid(["X...", ".M..", "..A.", "...S"], 4, 4).search_for_xmas() == 1
    assert Grid(["X...", "M...", "A...", "S..."], 4, 4).search_for_xmas() == 1
    assert Grid(["...X", "..M.", ".A..", "S..."], 4, 4).search_for_xmas() == 1
    assert Grid(["SAMX", "....", "....", "...."], 4, 4).search_for_xmas() == 1
    assert Grid(["S...", ".A..", "..M.", "...X"], 4, 4).search_for_xmas() == 1
    assert Grid(["S...", "A...", "M...", "X..."], 4, 4).search_for_xmas() == 1
    assert Grid(["...S", "..A.", ".M..", "X..."], 4, 4).search_for_xmas() == 1


def test_search_nb_cross_mas_in_grid():
    assert Grid(["...", "...", "..."], 3, 3).search_for_cross_mas() == 0
    assert Grid(["S.S", ".A.", "M.M"], 3, 3).search_for_cross_mas() == 1
    assert Grid(["S.M", ".A.", "S.M"], 3, 3).search_for_cross_mas() == 1
    assert Grid(["M.M", ".A.", "S.S"], 3, 3).search_for_cross_mas() == 1
    assert Grid(["M.S", ".A.", "M.S"], 3, 3).search_for_cross_mas() == 1


if __name__ == "__main__":
    grid_sample: Grid = parse_data("data/day4-sample")
    grid: Grid = parse_data("data/day4")

    test_search_nb_xmas_in_grid()
    assert grid_sample.search_for_xmas() == 18

    test_search_nb_cross_mas_in_grid()
    assert grid_sample.search_for_cross_mas() == 9

    logger.info(f"Day 4a > {grid.search_for_xmas()}")
    logger.info(f"Day 4b > {grid.search_for_cross_mas()}")
