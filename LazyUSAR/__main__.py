import keyboard
from . import jumping_jacks
from time import sleep


SLEEP_TIME = 0.1


class UI:
    def __init__(
        self,
        exit_key: str,
    ):
        self.__exit_key = exit_key
        print(f"Press {exit_key} to exit")

        self.running = True
        keyboard.hook(self.on_key_event)

        self.temp = jumping_jacks.JumpingJackController(
            500, 1, 10, jumping_jacks.JumpingJackType.UPPERCASE, True, False
        )
        self.temp.start()
        self.block_until_stopped()

    def block_until_stopped(self):
        while self.running:
            sleep(SLEEP_TIME)

    def on_key_event(self, key: keyboard.KeyboardEvent):
        if key.event_type != "down":
            return
        if key.name == self.__exit_key:
            self.temp.exit()
            self.running = False


def main():
    UI("f6")


if __name__ == "__main__":
    main()
