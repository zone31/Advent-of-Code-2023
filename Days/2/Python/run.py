#!/usr/bin/env python3
import os
import sys

####################### Helping functions###########################


def data_parser(filepath) -> dict[list[dict[str, int]]]:
    """Parse the data by splitting each line into a number."""
    with open(filepath, "r") as file:
        data = file.read()
        split = data.split("\n")
        ret = {}
        for game in split:
            game_id, game_data = game.split(":")
            game_id = int(game_id[5:])
            grabs = game_data.split(";")
            ret_game = []
            for grab in grabs:
                ret_grab = {}
                for elem in grab.split(","):
                    val, color = elem[1:].split(" ")
                    ret_grab[color] = int(val)
                ret_game.append(ret_grab)
            ret[game_id] = ret_game
        return ret


######################### Main functions############################


def solver_1star(data: dict[list[dict[str, int]]]):
    """
    Iterate over each game, and find the target
    """
    target = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    ret = []
    for game_id, game in data.items():
        valid = True
        for grab in game:
            if not all([target[color] >= val for color, val in grab.items()]):
                valid = False
                break
        if valid:
            ret.append(game_id)
    return sum(ret)


def solver_2star(data: list[str]):
    """
    Iterate over each game, observe the lowest value per grab
    """
    ret = []
    for game_id, game in data.items():
        biggest_seen = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }
        for grab in game:
            for color, val in grab.items():
                if biggest_seen[color] < val:
                    biggest_seen[color] = val
        game_ret = 1
        for value in biggest_seen.values():
            game_ret = game_ret * value
        ret.append(game_ret)
    return sum(ret)


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
