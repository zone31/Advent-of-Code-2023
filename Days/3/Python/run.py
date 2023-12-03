#!/usr/bin/env python3
from collections import defaultdict
import itertools
import os
import sys
from typing import Any, TypeVar

####################### Helping functions###########################


def data_parser(filepath) -> list[list[str]]:
    """Parse the data by splitting each line into a number."""
    with open(filepath, "r") as file:
        data = file.read()
        split = data.split("\n")
        ret = []
        for line in split:
            ret.append([x for x in line])
        return ret


T = TypeVar("T")


def get_sub_schematic(
    data: dict[tuple[int, int], T], point: tuple[int, int]
) -> dict[tuple[int, int], T]:
    x, y = point
    ret = {}
    for yd in range(y - 1, y + 2):
        for xd in range(x - 1, x + 2):
            if (xd, yd) in data:
                ret[(xd, yd)] = data[(xd, yd)]
    return ret


def find_number_pos(
    data: dict[tuple[int, int], int], point: tuple[int, int]
) -> dict[tuple[int, int], int]:
    if point not in data:
        return {}
    # First backwards, then forwards
    ret = {}
    ret[point] = data[point]
    x, y = point
    for xd in itertools.count(x):
        if (xd, y) not in data:
            break
        ret[(xd, y)] = data[(xd, y)]
    for xd in itertools.count(x, -1):
        if (xd, y) not in data:
            break
        ret[(xd, y)] = data[(xd, y)]

    return ret


def generate_table(
    data: list[list[str]],
) -> tuple[dict[tuple[int, int], str], dict[tuple[int, int], int]]:
    # Generate a cord table with the elements, and
    # lookup for the symbols
    numbers = dict()
    symbols = dict()
    all_data = dict()
    for y, row in enumerate(data):
        for x, elem in enumerate(row):
            point = (x, y)
            if elem == ".":
                continue
            if elem.isdigit():
                numbers[point] = int(elem)
            else:
                symbols[point] = elem
    return (symbols, numbers)


def pr(data):
    x_max, y_max = 0, 0
    for (xd, yd), val in data.items():
        x_max = xd if xd > x_max else x_max
        y_max = yd if yd > y_max else y_max

    for y in range(y_max + 1):
        for x in range(x_max + 1):
            point = (x, y)
            if point in data:
                print(data[point], end="")
            else:
                print(".", end="")
        print("\n", end="")


######################### Main functions############################


def solver_1star(data: list[list[str]]):
    """
    Dump the data in a hashmap of the positions, get elements the position
    can see, use those positions to get the positions of a number.
    Only include numbers you have seen around a symbol
    """
    symbols, numbers = generate_table(data)

    # Now that we have a board representation, go over each symbol
    # and mark numbers that we have hit
    numbers_touched = dict()
    for pos, item in symbols.items():
        sub_area = get_sub_schematic(numbers, pos)
        # detect all numbers in the sub area
        for sub_pos, sub_item in sub_area.items():
            numbers_touched.update(find_number_pos(numbers, sub_pos))

    # Sort each missing element into their own number
    numbers_touched_set = set()
    for elem in numbers_touched.keys():
        numbers_touched_set.add(frozenset(find_number_pos(numbers, elem).keys()))

    # Now that we have a set of number poses separated, we convert them to numbers and print them
    ret = 0
    for numbers_touched_elem in numbers_touched_set:
        elem = 0
        for pos in sorted(list(numbers_touched_elem), key=lambda x: x[0]):
            elem = elem * 10 + numbers[pos]
        ret += elem

    return ret


def solver_2star(data: list[list[str]]):
    """
    Same as above, but detect only one symbol "*", and only do the operation
    if 2 numbers are found around the symbol
    """
    symbols, numbers = generate_table(data)
    ret = 0

    # Go over each multiply symbol, and get the list of numbers around
    for pos, val in symbols.items():
        if val != "*":
            continue
        sub_area = get_sub_schematic(numbers, pos)
        # detect all numbers in the sub area
        numbers_touched_set = set()
        for sub_pos, sub_item in sub_area.items():
            numbers_touched_set.add(frozenset(find_number_pos(numbers, sub_pos).keys()))
        related_numbers = [
            sorted(list(x), key=lambda y: y[0]) for x in numbers_touched_set
        ]
        # If we see 2 numbers, do the multiplication
        if len(related_numbers) == 2:
            elem_ret = 1
            for related_number in related_numbers:
                elem = 0
                for related_pos in related_number:
                    elem = elem * 10 + numbers[related_pos]
                elem_ret *= elem

            ret += elem_ret
    return ret


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
