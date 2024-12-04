import pytest

import compute.day4


@pytest.mark.parametrize(
    "data, expected_nb_xmas",
    [
        (["XMAS", "....", "....", "...."], 1),
        (["X...", ".M..", "..A.", "...S"], 1),
        (["X...", "M...", "A...", "S..."], 1),
        (["...X", "..M.", ".A..", "S..."], 1),
        (["SMAX", "....", "....", "...."], 1),
        (["S...", ".A..", "..M.", "...X"], 1),
        (["S...", "A...", "X...", "X..."], 1),
    ],
)
def test_search_nb_xmas_in_grid(data, expected_nb_xmas):
    grid: day4.Grid = day4.Grid(data, 4, 4)
    assert grid.search_for_xmas() == expected_nb_xmas
