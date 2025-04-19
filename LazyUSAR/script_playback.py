from time import sleep
from . import system_controller
from .counter_types import ControlledIntervaledCounter

DELAY_MS = 150


class ScriptPlaybackController:
    def _initialize(
        self,
        end_callback: callable,
        playback_callback: callable,
        interval: int,
        script: str,
        username: str,
        rank: str,
    ):
        self.interval = interval * 1000  # Convert to milliseconds
        script = script.replace("<username>", username)
        script = script.replace("<name>", username)
        script = script.replace("<rank>", rank)
        self.script_array = list(
            filter(lambda line: line.strip() != "", script.splitlines())
        )
        self.username = username
        self.rank = rank
        self.playback_callback = playback_callback
        self.end_callback = end_callback
        self.counter = ControlledIntervaledCounter(
            self._send_script_line,
            0,
            self.interval,
            stop_count=len(self.script_array) - 1,
            backward_key="j",
            toggle_key="k",
            forward_key="l",
            step=1,
        )

    def __init__(
        self,
        end_callback: callable,
        playback_callback: callable,
        interval: int,
        script: str,
        username: str,
        rank: str,
    ):
        self._initialize(
            end_callback, playback_callback, interval, script, username, rank
        )

    def remake(
        self,
        interval: int,
        script: str,
        username: str,
        rank: str,
    ):
        self.exit()
        self._initialize(
            self.end_callback, self.playback_callback, interval, script, username, rank
        )

    def _send_script_line(self, line_num: int):
        # Press /, then copy the line, then paste the line, then press enter
        system_controller.press("/")
        sleep(DELAY_MS / 1000)
        system_controller.copy(self.script_array[line_num])
        system_controller.paste()
        system_controller.press("enter")
        self.playback_callback(self.script_array[line_num], line_num)
        if line_num + 1 >= len(self.script_array):
            self.reset()
            self.end_callback()

    def start(self):
        if len(self.script_array) == 0:
            print("No script lines to send.")
            self.end_callback()
            return
        system_controller.running = True
        self.counter.start()

    def stop(self):
        self.exit()

    def exit(self):
        system_controller.running = False
        self.counter.exit()

    def reset(self):
        self.counter.reset()

    def toggle(self) -> bool:
        if len(self.script_array) == 0:
            return False
        if self.counter.is_listening:
            self.stop()
            return False
        else:
            self.start()
            return True
