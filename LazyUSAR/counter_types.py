# Two shared action types
from threading import Timer
import keyboard


class ControlledCounter:
    def __init__(
        self,
        callback: callable,
        start_count: int,
        backward_key: str,
        toggle_key: str,
        forward_key: str,
        step=1,
    ):
        self.callback = callback
        self.start_count = start_count
        self.backward_key = backward_key
        self.toggle_key = toggle_key
        self.forward_key = forward_key
        self.count = self.start_count
        self.step = step
        self.listener_hook = None

    def reset(self):
        self.count = self.start_count

    def start(self):
        self.listener_hook = keyboard.hook(self.on_key_event)

    def on_key_event(self, key: keyboard.KeyboardEvent):
        if key.event_type != "down":  # Only on key down events
            return
        if key.name == self.toggle_key:
            self.callback(self.count)
            self.count += self.step
        elif key.name == self.backward_key:
            self.count -= self.step
        elif key.name == self.forward_key:
            self.count += self.step

    def exit(self):
        if self.listener_hook is not None:
            keyboard.unhook(self.listener_hook)
        self.listener_hook = None


class ControlledIntervaledCounter(ControlledCounter):
    def __init__(
        self,
        callback: callable,
        start_count: int,
        interval: int,
        backward_key,
        toggle_key,
        forward_key,
        step=1,
    ):
        self.running = False
        self.interval = interval
        super().__init__(
            callback, start_count, backward_key, toggle_key, forward_key, step
        )

    def _set_interval(self):
        if self.running:
            self.callback(self.count)
            self.count += self.step
            self.timer = Timer(self.interval / 1000, self._set_interval)
            self.timer.start()

    def _stop_interval(self):
        if hasattr(self, "timer"):
            self.timer.cancel()

    def on_key_event(self, key):
        if key.event_type != "down":
            return
        if key.name == self.toggle_key:
            self.running = not self.running
            if self.running:
                self._set_interval()
            else:
                self._stop_interval()
        elif key.name == self.backward_key:
            self.count -= self.step
        elif key.name == self.forward_key:
            self.count += self.step

    def exit(self):
        if self.listener_hook is not None:
            keyboard.unhook(self.listener_hook)
        self.listener_hook = None
        self.running = False
