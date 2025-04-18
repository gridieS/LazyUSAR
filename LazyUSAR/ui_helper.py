import sys
import os
import tkinter as tk


def load_asset(path):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    assets = os.path.join(base, "assets")
    return os.path.join(assets, path)


class Checkbox(tk.Checkbutton):
    def __init__(self, callback, checked=False, args=[], mini=False):
        self.state = tk.IntVar()
        if mini:
            self.checked_image = tk.PhotoImage(file=load_asset("mini_checked.png"))
            self.unchecked_image = tk.PhotoImage(file=load_asset("mini_unchecked.png"))
        else:
            self.checked_image = tk.PhotoImage(file=load_asset("checked.png"))
            self.unchecked_image = tk.PhotoImage(file=load_asset("unchecked.png"))
        super().__init__(
            image=self.unchecked_image,
            selectimage=self.checked_image,
            indicatoron=False,
            borderwidth=0,
            command=self.on_press,
            cursor="hand2",
            variable=self.state,
        )
        self.args = args
        self.callback = callback
        if checked:
            self.toggle()

    def toggle_callback(self):
        self.toggle()
        self.callback(self.state.get(), *self.args)

    def set(self, value: bool, trigger_callback=False):
        if self.state.get() != value:
            if trigger_callback:
                self.toggle_callback()
            else:
                self.toggle()

    def on_press(self):
        self.toggle()
        self.toggle_callback()
