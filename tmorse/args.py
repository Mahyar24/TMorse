#! /usr/bin/python3.9

"""
Mahyar@Mahyar24.com, Wed 01 Dec 2021.
"""

import argparse
import pathlib
import textwrap


def parse_args() -> argparse.Namespace:
    """
    Parsing the passed arguments, read help (-h, --help) for further information.
    """
    parser = argparse.ArgumentParser(
        epilog=textwrap.dedent(
            """
            Written by: Mahyar Mahdavi <Mahyar@Mahyar24.com>.
            License: GNU GPLv3.
            Source Code: <https://github.com/mahyar24/TMorse>.
            PyPI: <https://pypi.org/project/TMorse/>.
            Reporting Bugs and PRs are welcomed. :)
            """
        )
    )

    input_args = parser.add_mutually_exclusive_group()

    parser.add_argument(
        "-m",
        "--multiplier",
        default=0.15,
        type=float,
        help="Select desired multiplier for timing.",
    )

    parser.add_argument(
        "--on-command",
        default="0 on",
        help="Command for writing ON in file descriptor.",
    )

    parser.add_argument(
        "--off-command",
        default="0 off",
        help="Command for writing OFF in file descriptor.",
    )

    parser.add_argument(
        "--default-led-status",
        default="ON",
        type=lambda x: x.upper(),
        choices=["ON", "OFF"],
        help="Led status after blinking finished.",
    )

    parser.add_argument(
        "-l",
        "--led-path",
        default="/proc/acpi/ibm/led",
        type=pathlib.Path,
        help="Specify led path for blinking.",
    )

    parser.add_argument(
        "-c",
        "--codes-file",
        type=pathlib.Path,
        help="Path to a json file which contains morse codes for every character."
        " Default file only supports ASCII characters.",
    )

    input_args.add_argument(
        "-i",
        "--input",
        type=pathlib.Path,
        help="Read input from a file.",
    )

    input_args.add_argument(
        "-s",
        "--stdin",
        action="store_true",
        default=False,
        help="Read input from standard input.",
    )

    input_args.add_argument(
        "--hidden",
        action="store_true",
        default=False,
        help="Getting input characters in secret mode. (hidden)",
    )

    return parser.parse_args()
