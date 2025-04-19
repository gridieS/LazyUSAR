# Code generated by TkForge <https://github.com/axorax/tkforge>

import tkinter as tk
from tkinter.filedialog import askopenfilename
import keyboard

from .ui_helper import Checkbox, load_asset
from .script_playback import ScriptPlaybackController

DEFAULT_INTERVAL_TIME = 2
MIN_INTERVAL_TIME = 0.5

DEFAULT_SCRIPT_METHOD = "file"
DEFAULT_FILE_TEXT = "No file chosen"

DEFAULT_USERNAME_TEXT = "YourName"
DEFAULT_RANK_TEXT = "YourRank"

DEFAULT_LINE_NUM = 0
DEFAULT_LINE_TEXT = "The script line will appear here"


class ScriptPlaybackUI:
    def __init__(
        self,
        exit_key: str,
        toggle_key: str,
        switch_callback: callable,
    ):
        self.switch_callback = switch_callback
        self.toggle_key = toggle_key

        self.cur_file_path = ""
        self.cur_line = ""
        self.cur_line_num = DEFAULT_LINE_NUM
        self.script = ""
        self.script_playback_controller = ScriptPlaybackController(
            self.toggle_controller,
            self.script_playback_callback,
            DEFAULT_INTERVAL_TIME,
            "",
            DEFAULT_USERNAME_TEXT,
            DEFAULT_RANK_TEXT,
        )

        self.exit_key = exit_key
        self.controller_running = False
        keyboard.hook(self.on_key_event)

    def start(self):

        self.window = tk.Tk()
        self.window.geometry("615x745")
        self.window.configure(bg="#d4d4d4")
        self.window.title("Tkinter Export")

        canvas = tk.Canvas(
            self.window,
            bg="#c5c5c5",
            width=615,
            height=745,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        canvas.place(x=0, y=0)

        canvas.create_text(
            274,
            82,
            anchor="nw",
            text="Options",
            fill="#000000",
            font=("Inter", 18 * -1),
        )

        canvas.create_text(
            283,
            364,
            anchor="nw",
            text="Script",
            fill="#000000",
            font=("Inter", 18 * -1),
        )

        canvas.create_line(51, 349, 562, 349, fill="#000000", width=0.75)
        canvas.create_line(51, 111, 562, 111, fill="#000000", width=0.75)
        canvas.create_line(51, 111, 52, 349, fill="#000000", width=0.75)
        canvas.create_line(563, 111, 563, 349, fill="#000000", width=0.75)

        canvas.create_text(
            413, 129, anchor="nw", text="Rank", fill="#000000", font=("Inter", 18 * -1)
        )
        canvas.create_text(
            326,
            201,
            anchor="nw",
            text="(Replaces <rank> in text)",
            fill="#000000",
            font=("Inter", 18 * -1),
        )

        self.rank_entry = tk.Entry(
            bg="#d9d9d9",
            borderwidth=2.25,
            justify="center",
            relief="solid",
            highlightbackground="black",
            insertbackground="#000000",
            font="Inter 14",
        )

        self.rank_entry.place(x=332, y=158, width=206, height=33)

        canvas.create_text(
            137,
            129,
            anchor="nw",
            text="Username",
            fill="#000000",
            font=("Inter", 18 * -1),
        )

        canvas.create_text(
            72,
            201,
            anchor="nw",
            text="(Replaces <user> in text)",
            fill="#000000",
            font=("Inter", 18 * -1),
        )

        self.username_entry = tk.Entry(
            bd=0,
            bg="#d9d9d9",
            borderwidth=2.25,
            justify="center",
            relief="solid",
            highlightbackground="black",
            insertbackground="#000000",
            font="Inter 14",
        )

        self.username_entry.place(x=78, y=158, width=206, height=33)

        self.interval_entry = tk.Entry(
            bd=0,
            bg="#d9d9d9",
            borderwidth=2.25,
            justify="center",
            relief="solid",
            highlightbackground="black",
            insertbackground="#000000",
            font="Inter 14",
        )

        self.interval_entry.place(x=204, y=271, width=206, height=33)

        canvas.create_text(
            274,
            242,
            anchor="nw",
            text="Interval",
            fill="#000000",
            font=("Inter", 18 * -1),
        )

        canvas.create_text(
            271,
            314,
            anchor="nw",
            text="Seconds",
            fill="#000000",
            font=("Inter", 18 * -1),
        )

        self.toggle_button_label = tk.Label(
            text=f"Press {self.toggle_key.upper()} to start",
            fg="#000000",
            bg="#d9d9d9",
            relief="solid",
            borderwidth="2.25",
            font=("Inter", -18),
        )

        self.toggle_button_label.place(x=139, y=30, width=340, height=37)
        self.toggle_button_label.bind("<Button-1>", lambda _: self.toggle_controller())

        self.text_method_checkbox = Checkbox(
            self.toggle_script_method_pressed, args=["text"], mini=True
        )
        self.text_method_checkbox.place(x=515, y=425, width=25, height=25)

        canvas.create_text(
            512, 403, anchor="nw", text="Text", fill="#000000", font=("Inter", 15 * -1)
        )

        self.file_method_checkbox = Checkbox(
            self.toggle_script_method_pressed, args=["file"], mini=True
        )
        self.file_method_checkbox.place(x=76, y=425, width=25, height=25)

        canvas.create_text(
            75, 403, anchor="nw", text="File", fill="#000000", font=("Inter", 15 * -1)
        )

        self.line_label = tk.Label(
            text=DEFAULT_LINE_TEXT,
            justify="center",
            bg="#C5C5C5",
            font=("Inter", 14 * -1),
            wraplength=471,
        )
        self.line_label.place(x=72, y=534, width=471, height=50)

        self.line_num_label = tk.Label(
            text="111",
            justify="center",
            bg="#C5C5C5",
            font=("Inter", 16 * -1),
        )
        self.line_num_label.place(x=306, y=516, width=25, height=25, anchor="center")

        self.reset_button = tk.Label(
            text="Reset",
            relief="solid",
            borderwidth="2.25",
            justify="center",
            bg="#d9d9d9",
            font=("Inter", 18 * -1),
        )

        self.reset_button.place(x=260, y=594, width=96, height=37)
        self.reset_button.bind("<Button-1>", lambda _: self.set_defaults())

        self.file_text_label = tk.Label(
            justify="center",
            text=DEFAULT_FILE_TEXT,
            bg="#c5c5c5",
            font=("Inter 10"),
        )

        self.file_text_label.place(x=307, y=463, width=486, height=18, anchor="center")

        # def center_text(event): # Uncomment this if you think centered text is better
        #     self.text_method.tag_add("center", "1.0", "end")
        #     self.text_method.edit_modified(False)  # reset the modified flag
        # self.text_method.tag_configure("center", justify="center")
        # self.text_method.tag_add("center", "1.0", "end")
        # self.text_method.bind("<<Modified>>", center_text)

        def text_method_focus_out(event):
            self.script = self.text_method.get("1.0", "end-1c")
            self.remake_controller()

        self.text_method = tk.Text(
            bg="#d9d9d9",
            relief="solid",
            borderwidth="2.25",
            highlightbackground="black",
            insertbackground="#000000",
            highlightthickness=0,
        )
        self.text_method.place(x=126, y=410, width=364, height=98)
        self.text_method.bind("<FocusOut>", text_method_focus_out)

        def choose_file_button_pressed(event):
            file_path = askopenfilename()
            if len(file_path) == 0:
                return
            if self.cur_file_path == file_path or not file_path.endswith(
                (".txt", ".md")
            ):
                return
            try:
                with open(file_path, "rb") as file:
                    content = file.read()
                    self.cur_file_path = file_path
                    self.script = content.decode("utf-8", errors="ignore")
                    self.cur_line_num = 1
            except Exception as e:
                print(f"Error reading file: {e}")

            self.remake_controller()
            self.update_preview()

        self.choose_file_button = tk.Label(
            text="Choose file",
            bg="#d9d9d9",
            justify="center",
            relief="solid",
            borderwidth="2",
            font=("Inter", -12),
        )

        self.choose_file_button.place(x=265, y=479, width=85, height=25)
        self.choose_file_button.bind("<Button-1>", choose_file_button_pressed)

        canvas.create_line(54, 640, 565, 640, fill="#000000", width=0.75)
        canvas.create_line(54, 396, 565, 396, fill="#000000", width=0.75)
        canvas.create_line(53, 397, 53, 641, fill="#000000", width=0.75)
        canvas.create_line(565, 396, 565, 640, fill="#000000", width=0.75)

        def switch_button_pressed():
            self.exit()
            self.switch_callback()

        switch_image = tk.PhotoImage(file=load_asset("switch.png"))

        switch_button = tk.Button(
            image=switch_image,
            bg="#d9d9d9",
            relief="solid",
            borderwidth=2.25,
            padx=50,
            pady=50,
            command=switch_button_pressed,
        )

        switch_button.place(x=307, y=699, width=52, height=52, anchor="center")

        self.set_defaults()

        self.window.resizable(False, False)
        self.window.mainloop()

    def check_parameters(self):
        if (
            self.interval_entry.get() == ""
            or self.username_entry.get() == ""
            or self.rank_entry.get() == ""
        ):
            return False
        elif (
            not "".join(self.interval_entry.get().split(".")).strip().isnumeric()
        ):  # Removed any whitespaces and dots, joins, and checks if is numeric
            return False
        elif float(self.interval_entry.get()) < MIN_INTERVAL_TIME:
            return False

        return True

    def toggle_controller(self):
        if not self.check_parameters():
            return
        self.controller_running = self.script_playback_controller.toggle()
        if self.controller_running:
            toggle_text = f"Press {self.toggle_key.upper()} to stop"
            self.script_playback_controller.start()
        else:
            toggle_text = f"Press {self.toggle_key.upper()} to start"
            self.script_playback_controller.stop()

        self.toggle_button_label.config(text=toggle_text)

    def remake_controller(self):
        paramaters_changed = (
            float(self.script_playback_controller.interval / 1000)
            != float(self.interval_entry.get())
            or self.script_playback_controller.username != self.username_entry.get()
            or self.script_playback_controller.rank != self.rank_entry.get()
            or self.script_playback_controller.script_array == []
        )
        if paramaters_changed:
            self.script_playback_controller.remake(
                float(self.interval_entry.get()),
                self.script,
                self.username_entry.get(),
                self.rank_entry.get(),
            )

    def toggle_script_method_pressed(self, value: bool, method: str):
        if value == False:
            self.cur_method.set(True)
        else:
            self.cur_method.set(False)
            match (method):
                case "text":
                    self.cur_method = self.text_method_checkbox
                    self.file_text_label.place_forget()
                    self.text_method.place(x=126, y=410, width=364, height=98)
                    self.choose_file_button.place_forget()
                case "file":
                    self.cur_method = self.file_method_checkbox
                    self.text_method.place_forget()
                    self.file_text_label.place(
                        x=307, y=463, width=486, height=18, anchor="center"
                    )
                    self.choose_file_button.place(x=265, y=479, width=85, height=25)

    def set_file_defaults(self):
        self.script_playback_controller.exit()
        if self.controller_running:
            self.toggle_controller()

        self.cur_file_path = DEFAULT_FILE_TEXT
        self.cur_line = DEFAULT_LINE_TEXT
        self.cur_line_num = int(DEFAULT_LINE_NUM)
        self.script = ""

        self.update_preview()

    def set_defaults(self):
        self.interval_entry.delete(0, tk.END)
        self.interval_entry.insert(tk.END, str(DEFAULT_INTERVAL_TIME))
        self.interval_entry.bind("<Return>", lambda _: self.remake_controller())
        self.interval_entry.bind("<FocusOut>", lambda _: self.remake_controller())

        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(tk.END, DEFAULT_USERNAME_TEXT)
        self.username_entry.bind("<Return>", lambda _: self.remake_controller())
        self.username_entry.bind("<FocusOut>", lambda _: self.remake_controller())

        self.rank_entry.delete(0, tk.END)
        self.rank_entry.insert(tk.END, DEFAULT_RANK_TEXT)
        self.rank_entry.bind("<Return>", lambda _: self.remake_controller())
        self.rank_entry.bind("<FocusOut>", lambda _: self.remake_controller())

        if DEFAULT_SCRIPT_METHOD == "text":
            self.cur_method = self.text_method_checkbox
        elif DEFAULT_SCRIPT_METHOD == "file":
            self.cur_method = self.file_method_checkbox
            self.set_file_defaults()
        self.toggle_script_method_pressed(True, DEFAULT_SCRIPT_METHOD)
        self.cur_method.set(True)

        self.update_preview()

    def update_preview(self):
        self.file_text_label.config(text=self.cur_file_path)
        self.line_label.config(text=self.cur_line)
        self.line_num_label.config(text=str(self.cur_line_num))

    def script_playback_callback(self, line: str, line_num: int):
        self.cur_line = line
        self.cur_line_num = line_num + 1
        self.update_preview()

    def on_key_event(self, key: keyboard.KeyboardEvent):
        if key.event_type != "down":
            return
        if key.name == self.exit_key:
            self.exit()
        if key.name == self.toggle_key:
            self.toggle_controller()

    def exit(self):
        keyboard.unhook(self.on_key_event)
        self.script_playback_controller.exit()
        self.window.destroy()
