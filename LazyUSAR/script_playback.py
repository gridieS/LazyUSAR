# Process file, move to array
# For each i, copy array[i] to clipboard
# Enter chat, paste from clipboard
# Do until done


class ScriptPlaybackController:
    def __init__(
        self,
        end_callback: callable,
    ):
        self.islistening = False
        self.end_callback = end_callback

    def start(self):
        print("Started")

    def stop(self):
        self.exit()

    def exit(self):
        print("Exited")

    def toggle(self) -> bool:
        self.islistening = not self.islistening
        return self.islistening
