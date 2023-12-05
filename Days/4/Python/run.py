#!/usr/bin/env python3
import itertools
import os
import sys
from collections import defaultdict
from functools import cache
from typing import Any, TypeVar

####################### Helping functions###########################


def data_parser(filepath) -> dict[int, tuple[list[int], list[int]]]:
    """Parse the data by splitting each line into a number."""
    with open(filepath, "r") as file:
        data = file.read()
        split = data.split("\n")
        ret = {}
        for lotto in split:
            lotto_id, lotto_data = lotto.split(":")
            lotto_id = int(lotto_id[5:])
            lotto_win, lotto_draw = lotto_data.split("|")

            lotto_win_parsed = [int(x) for x in lotto_win.split(" ") if x != ""]
            lotto_draw_parsed = [int(x) for x in lotto_draw.split(" ") if x != ""]
            ret[lotto_id] = (lotto_win_parsed, lotto_draw_parsed)
        return ret


######################### Main functions############################


def solver_1star(data: dict[int, tuple[list[int], list[int]]]):
    """
    Get the draws and winnings, make them into a set, and compare
    the missing elements. point them accordingly
    """
    ret = 0
    for lotto_id, (win, draw) in data.items():
        missing = set(win) - set(draw)
        points = len(set(win)) - len(missing)
        if points > 0:
            ret += 2 ** (points - 1)
    return ret


def solver_2star(data: dict[int, tuple[list[int], list[int]]]):
    """
    Go over each element, and keep track from top to bottom,
    if we have won. Add additional cards based on this.
    """
    win_relations = dict()
    for lotto_id, (win, draw) in data.items():
        missing = set(win) - set(draw)
        points = len(set(win)) - len(missing)
        hits = [x + 1 + lotto_id for x in range(points)]
        if len(hits) > 0:
            win_relations[lotto_id] = hits

    have = {x: 1 for x in data.keys()}

    for n in data.keys():
        # Run the iteration the amount as many times as we have cards
        for _ in range(have[n]):
            if n in win_relations:
                for j in win_relations[n]:
                    have[j] += 1

    return sum([x for x in have.values()])


############################## MAIN#################################


def main(solve=0):
    """Run the program by itself, return a tuple of star1 and star2.

    solve: set what stars we want, 0 returns both
    """
    dirname = os.path.dirname(__file__)
    input_source = os.path.join(dirname, "..", "input1.txt")
    # Make list, since the generator has to be used multiple times
    data = data_parser(input_source)
    match solve:
        case 0:
            return (solver_1star(data), solver_2star(data))
        case 1:
            return (solver_1star(data), None)
        case 2:
            return (None, solver_2star(data))
        case _:
            raise Exception(f"solve set wrong! ({solve})")


def day_name():
    """Get the date name from the folder."""
    file_path = os.path.dirname(__file__)
    day_path = os.path.normpath(os.path.join(file_path, ".."))
    return os.path.basename(day_path)


if __name__ == "__main__":
    solve = 0
    if len(sys.argv) == 2:
        solve = int(sys.argv[1])
    star1, star2 = main(solve)

    match solve:
        case 0:
            day = day_name()
            print(f"Day {day} first star:")
            print(star1)
            print(f"Day {day} second star:")
            print(star2)
        case 1:
            print(star1)
        case 2:
            print(star2)
        case _:
            raise Exception(f"solve set wrong! ({solve})")
