import sys
import subprocess
import time

IS_WINDOWS = sys.platform.startswith("win")
IS_LINUX = sys.platform.startswith("linux")

DELAY_MS = 30

if IS_WINDOWS:
    import pydirectinput as pdi

    pdi.PAUSE = DELAY_MS / 1000 / 2


def _run_cmd(cmd: list[str]):
    """Run a shell command quietly."""
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[system_controller] Error running command: {cmd}\n{e}")


if IS_LINUX:
    _run_cmd(["setxkbmap", "us"])


SHIFT_KEY = "shift"
WINDOWS_SPECIAL_CHARACTERS = {
    "!": "1",
    "@": "2",
    "#": "3",
    "$": "4",
    "A": "a",
    "B": "b",
    "C": "c",
    "D": "d",
    "E": "e",
    "F": "f",
    "G": "g",
    "H": "h",
    "I": "i",
    "J": "j",
    "K": "k",
    "L": "l",
    "M": "m",
    "N": "n",
    "O": "o",
    "P": "p",
    "Q": "q",
    "R": "r",
    "S": "s",
    "T": "t",
    "U": "u",
    "V": "v",
    "W": "w",
    "X": "x",
    "Y": "y",
    "Z": "z",
}


def write(text: str) -> None:
    """Type out a string of text."""
    if IS_WINDOWS:
        special_keys = WINDOWS_SPECIAL_CHARACTERS.keys()
        for char in text:
            if char in special_keys:
                key = WINDOWS_SPECIAL_CHARACTERS[char]
                pdi.keyDown(SHIFT_KEY)
                pdi.press(key, interval=0)
                pdi.keyUp(SHIFT_KEY)
            else:
                pdi.press(char, interval=0)
    elif IS_LINUX:
        _run_cmd(["xdotool", "type", "--delay", str(DELAY_MS), text])


def press(key: str) -> None:
    """Press and release a key."""
    if IS_WINDOWS:
        pdi.press(key)
    elif IS_LINUX:
        if key == "/":
            key = "slash"
        _run_cmd(["xdotool", "key", key])


def hold(key: str) -> None:
    """Hold down a key."""
    if IS_WINDOWS:
        pdi.keyDown(key)
    elif IS_LINUX:
        _run_cmd(["xdotool", "keydown", key])


def release(key: str) -> None:
    """Release a held key."""
    if IS_WINDOWS:
        pdi.keyUp(key)
    elif IS_LINUX:
        _run_cmd(["xdotool", "keyup", key])
