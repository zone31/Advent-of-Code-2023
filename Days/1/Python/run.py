#!/usr/bin/env python3
import os
import sys

####################### Helping functions###########################


def data_parser(filepath) -> list[str]:
    """Parse the data by splitting each line into a number."""
    with open(filepath, "r") as file:
        data = file.read()
        ret = data.split("\n")
        return ret


######################### Main functions############################


def solver_1star(data: list[str]):
    """
    Iterate over each element, detect if the char is a digit, and
    take the start and end of that string
    """
    tmp = []
    for element in data:
        a = ""
        for char in element:
            if char.isdigit():
                a += char
        tmp.append(int(f"{a[0]}{a[-1]}"))
    return sum(tmp)


def solver_2star(data: list[str]):
    """
    Do the same as star 1, but do a string replace before, to
    replace the number names with actual numbers.

    We need to insert the old elements before and after the number,
    so cases like eighttwo1 gets both the "8" and "2"
    """
    tmp = []
    digit_replacer = {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",
    }
    for element in data:
        a = ""
        for num, string in digit_replacer.items():
            element = element.replace(string, f"{string}{num}{string}")
        for char in element:
            if char.isdigit():
                a += char
        tmp.append(int(f"{a[0]}{a[-1]}"))
    return sum(tmp)


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
