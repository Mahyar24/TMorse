#! /usr/bin/python3.9

"""
Run this code to blink your ThinkPad LED based on a Morse code!
Compatible with python3.9+. No third-party library is required, implemented in pure python.
Make sure that you have required permissions to write to led acpi file descriptor.

Installation:
    $ python3.9 -m pip install tmorse
Basic usage:
    $ sudo tmorse
        -> Insert input manually, and it will blink your LED, which is located by default values.
    $ echo "This is a test" | sudo tmorse --stdin
        -> Read from standard input.
    $ sudo tmorse -c custom_codes.json
        -> Encode characters to Morse based on your custom codes although
           you should follow the protocol.
           (e.g. {"م": "--"})
    $ sudo tmorse --on-command 2 --off-command 0 -l "/proc/acpi/ibm/kbdlight" -m 0.7 --default-led-status OFF
        -> Show the Morse code by keyboard's backlit blinking.

    See tmorse --help for additional information.

Caution: This Project is based and inspired by "Ritvars Timermanis"'s thinkmorse.
Take a look at: https://github.com/RichusX/thinkmorse
License: GPLv3.
Github: https://github.com/Mahyar24/TMorse
PyPI: https://pypi.org/project/TMorse/
Mahyar@Mahyar24.com, Wed 01 Dec 2021.
"""

import argparse
import getpass
import json
import os
import sys
import time
from typing import Final

from .args import parse_args

DOT_LENGTH: Final = 1
DASH_LENGTH: Final = 3
INNER_ELE_GAP: Final = 1
LETTER_GAP: Final = 3
WORD_GAP: Final = 7
LOOP_GAP: Final = 10


def check_presentation(character: str) -> bool:
    """
    Check if a single character is defined for Morse encoding.
    """
    return character.upper() in CODES.keys()


def check_input(text: str) -> bool:
    """
    Check if all characters are defined for Morse encoding.
    """
    return all(map(check_presentation, text.replace(" ", "")))


def text_to_morse(text: str) -> str:
    """
    Encode the text to morse codes.
    """
    result: str = ""
    for character in text.upper():
        if character == " ":
            result += "/"
        else:
            result += CODES[character] + " "
    return result


def get_data(args: argparse.Namespace) -> str:
    """
    Determine how we should get the entering data based on cli arguments and actually getting it.
    """
    if args.input:
        if args.input.is_file():
            with open(args.input, encoding='utf-8') as file:
                return file.read()
        raise ValueError(f"{args.input!r} is not a file!")

    if args.stdin:
        return sys.stdin.read()

    if args.hidden:
        return getpass.getpass("Here: ")

    return input("Here: ")


def on_led(args: argparse.Namespace) -> None:
    """
    Turn the LED on.
    """
    with open(args.led_path, "w", encoding='utf-8') as led:
        led.write(args.on_command)


def off_led(args: argparse.Namespace) -> None:
    """
    Turn the LED off.
    """
    with open(args.led_path, "w", encoding='utf-8') as led:
        led.write(args.off_command)


def print_on() -> None:
    """
    Printing a dot when LED is on.
    """
    print("Writing: .", end="\r", flush=True)


def print_off() -> None:
    """
    Printing a dash when LED is off.
    """
    print("Writing: -", end="\r", flush=True)


def blink(morse_code: str, args: argparse.Namespace) -> None:
    """
    Convert the morse code to blinks. This function's algorithm is created by "Ritvars Timermanis".
    """

    def on():
        on_led(args)
        print_on()

    def off():
        off_led(args)
        print_off()

    for index, code in enumerate(morse_code[:-1]):
        if code == ".":
            on()
            time.sleep(args.multiplier * DOT_LENGTH)
            off()

            if morse_code[index + 1] not in (" ", "/"):
                time.sleep(args.multiplier * INNER_ELE_GAP)

        elif code == "-":
            on()
            time.sleep(args.multiplier * DASH_LENGTH)
            off()

            if morse_code[index + 1] not in (" ", "/"):
                time.sleep(args.multiplier * INNER_ELE_GAP)

        elif code == " ":
            if morse_code[index + 1] != "/" and morse_code[index - 1] != "/":
                time.sleep(args.multiplier * LETTER_GAP)

        elif code == "/":
            time.sleep(args.multiplier * WORD_GAP)


def main(args: argparse.Namespace) -> None:
    """
    Main function. Glue everything together.
    """
    data = get_data(args).replace("\n", " ").strip()
    if not check_input(data):
        raise ValueError(
            "There are some characters that I don't know how to encode."
            " use '-c/--codes-file for a custom json encoding file.'"
        )

    morse_code = text_to_morse(data)

    try:
        blink(morse_code, args)
    except KeyboardInterrupt:
        pass
    finally:  # We should keep the light back to its default status no matter what.
        if args.default_led_status == "ON":
            on_led(args)
        else:
            off_led(args)


if __name__ == "__main__":
    ARGS = parse_args()

    assert os.access(
        ARGS.led_path, os.W_OK
    ), f"Permission is denied to write on {ARGS.led_path}"

    with open(ARGS.codes_file, encoding='utf-8') as json_file:
        CODES = json.load(json_file)

    main(ARGS)
