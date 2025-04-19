from time import sleep

from enum import Enum
from . import system_controller
from .counter_types import ControlledIntervaledCounter

DELAY_MS = 190

NUMBER_TO_WORDS = {
    0: "",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
    20: "twenty",
    30: "thirty",
    40: "forty",
    50: "fifty",
    60: "sixty",
    70: "seventy",
    80: "eighty",
    90: "ninety",
    100: "one hundred",
    200: "two hundred",
    300: "three hundred",
    400: "four hundred",
    500: "five hundred",
    600: "six hundred",
    700: "seven hundred",
    800: "eight hundred",
    900: "nine hundred",
}


def number_to_word(num: int, hyphebed: bool, end_of_word: str) -> str:
    num_in_words = ""
    if abs(num) < 20:
        num_in_words = NUMBER_TO_WORDS[abs(num)]
    else:
        num_to_str = str(abs(num))
        if int(num_to_str[-2] + num_to_str[-1]) < 20:
            num_in_words = (
                NUMBER_TO_WORDS[100 * int(num_to_str[-3])]
                + " "
                + NUMBER_TO_WORDS[int(num_to_str[-2] + num_to_str[-1])]
            )
        else:
            for i in range(len(num_to_str)):
                cur_word = NUMBER_TO_WORDS[
                    int(num_to_str[i]) * pow(10, len(num_to_str) - i - 1)
                ]
                if cur_word != "":
                    num_in_words += cur_word + " "
            num_in_words = num_in_words[:-1]

    if num < 0:
        num_in_words = "minus " + num_in_words
    if hyphebed:
        num_in_words = num_in_words.replace(" ", "-")
    num_in_words += end_of_word
    return num_in_words


def send_roblox_message(message: str):
    system_controller.press("/")
    sleep(DELAY_MS / 1000)
    system_controller.write(message)
    # Send the string
    sleep(DELAY_MS / 1000)
    system_controller.press("enter")


class JumpingJackType(Enum):
    UPPERCASE = 1
    LOWERCASE = 2
    HELL = 3
    NUMBER = 4
    GRAMMAR = 5

    def generator(self, num, hyphened: bool, end_of_word: str):
        self.end_of_word = end_of_word
        self.hyphened = hyphened
        if self is JumpingJackType.UPPERCASE:
            self._generator_uppercase(num)
        elif self is JumpingJackType.LOWERCASE:
            self._generator_lowercase(num)
        elif self is JumpingJackType.HELL:
            self._generator_helljack(num)
        elif self is JumpingJackType.NUMBER:
            self._generator_number(num)
        elif self is JumpingJackType.GRAMMAR:
            self._generator_grammar(num)
        else:
            raise NotImplementedError(f"Generator not implemented for {self.name}")

    def _default_jumping_jack(self, jj_str: str):
        send_roblox_message(jj_str)
        system_controller.press("space")  # On linux, this gets blocked often.

    def _generator_uppercase(self, count: int) -> str:
        self._default_jumping_jack(
            number_to_word(count, self.hyphened, self.end_of_word).upper()
        )

    def _generator_lowercase(self, count: int) -> str:
        self._default_jumping_jack(
            number_to_word(count, self.hyphened, self.end_of_word).lower()
        )

    def _generator_grammar(self, count: int) -> str:
        self._default_jumping_jack(
            number_to_word(count, self.hyphened, self.end_of_word).capitalize()
        )

    def _generator_helljack(self, count: int) -> str:
        iterable = list(number_to_word(count, False, "").replace(" ", "").upper())
        for i in iterable:
            send_roblox_message(i)
            system_controller.press("space")
        send_roblox_message(
            number_to_word(count, self.hyphened, self.end_of_word).upper()
        )
        system_controller.press("space")  # On linux, this gets blocked often.

    def _generator_number(self, count: int) -> str:
        num_str = str(count + self.end_of_word)
        self._default_jumping_jack(num_str)


class JumpingJackController:
    def _initialize(
        self,
        interval: int,
        starting_jj: int,
        ending_jj: int,
        jj_type: JumpingJackType | str,
        end_of_word: str,
        hyphened: bool,
        end_callback: callable,
        step=1,
    ):
        self.interval = interval
        self.starting_jj = starting_jj
        self.ending_jj = ending_jj
        if not isinstance(jj_type, JumpingJackType):
            jj_type = getattr(JumpingJackType, jj_type.upper())
        self.set_jj_type(jj_type)
        self.end_of_word = end_of_word
        self.hyphened = hyphened
        self.end_callback = end_callback
        self.counter = ControlledIntervaledCounter(
            self._perform_jumping_jack,
            self.starting_jj,
            self.interval,
            stop_count=self.ending_jj,
            backward_key="j",
            toggle_key="k",
            forward_key="l",
            step=step,
        )

    def __init__(
        self,
        interval: int,  # Milliseconds
        starting_jj: int,  # Including
        ending_jj: int,
        jj_type: JumpingJackType | str,
        end_of_word: str,
        hyphened: bool,
        end_callback: callable,
        step=1,
    ):
        self._initialize(
            interval,
            starting_jj,
            ending_jj,
            jj_type,
            end_of_word,
            hyphened,
            end_callback,
            step,
        )

    def remake(
        self,
        interval: int,
        starting_jj: int,
        ending_jj: int,
        jj_type: JumpingJackType | str,
        end_of_word: str,
        hyphened: bool,
        end_callback: callable,
        step=1,
    ):
        self.counter.exit()

        self._initialize(
            interval,
            starting_jj,
            ending_jj,
            jj_type,
            end_of_word,
            hyphened,
            end_callback,
            step,
        )

    def set_jj_type(self, jj_type: JumpingJackType):
        if not isinstance(jj_type, JumpingJackType):
            raise TypeError("Must be a JumpingJackType instance")
        self.__jj_type = jj_type

    def get_jj_type(self) -> JumpingJackType:
        return self.__jj_type

    def _perform_jumping_jack(self, count: int):
        self.__jj_type.generator(count, self.hyphened, self.end_of_word)
        if count + 1 > self.ending_jj:
            self.reset()
            self.end_callback()

    def reset(self):
        self.counter.reset()

    def start(self):
        system_controller.running = True
        self.counter.start()

    def stop(self):
        self.exit()

    # Returns running state after toggling
    def toggle(self) -> bool:
        if self.counter.is_listening:
            self.stop()
            return False
        else:
            self.start()
            return True

    def exit(self):
        system_controller.running = False
        self.counter.exit()
