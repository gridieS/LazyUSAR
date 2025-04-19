import sys
import subprocess
import pyperclip
from keyboard import press

IS_WINDOWS = sys.platform.startswith("win")
IS_LINUX = sys.platform.startswith("linux")

DELAY_MS = 30

if IS_WINDOWS:
    import pydirectinput as pdi

    pdi.PAUSE = DELAY_MS / 1000 / 2

running = True


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


# Adds clipboard support for both Windows and Linux using pyperclip
def copy(text: str) -> None:
    if not running:
        return
    try:
        pyperclip.copy(text)
    except pyperclip.PyperclipException as e:
        print(f"[system_controller] Error copying text to clipboard: {e}")


def paste() -> None:
    if not running:
        return
    try:
        if IS_LINUX:
            press("ctrl+v")
        elif IS_WINDOWS:
            pdi.hotkey("ctrl", "v")
    except pyperclip.PyperclipException as e:
        print(f"[system_controller] Error pasting text from clipboard: {e}")


def write(text: str) -> None:
    """Type out a string of text."""
    if not running:
        return
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
    if not running:
        return
    if IS_WINDOWS:
        pdi.press(key)
    elif IS_LINUX:
        if key == "/":
            key = "slash"
        _run_cmd(["xdotool", "key", key])


def hold(key: str) -> None:
    """Hold down a key."""
    if not running:
        return
    if IS_WINDOWS:
        pdi.keyDown(key)
    elif IS_LINUX:
        _run_cmd(["xdotool", "keydown", key])


def release(key: str) -> None:
    """Release a held key."""
    if not running:
        return
    if IS_WINDOWS:
        pdi.keyUp(key)
    elif IS_LINUX:
        _run_cmd(["xdotool", "keyup", key])
