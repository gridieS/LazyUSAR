from . import jumping_jack_ui, script_playback_ui


def switch_ui():
    global cur_ui
    if cur_ui == jumping_jack_ui_instance:
        cur_ui = script_playback_ui_instance
    elif cur_ui == script_playback_ui_instance:
        cur_ui = jumping_jack_ui_instance
    cur_ui()


def script_playback_ui_instance():
    script_playback_ui.ScriptPlaybackUI(
        "f6",
        "f5",
        switch_ui,
    ).start()


def jumping_jack_ui_instance():
    jumping_jack_ui.JumpingJackUI(
        "f6",
        "f5",
        switch_ui,
    ).start()


def main():
    global cur_ui
    try:
        cur_ui = jumping_jack_ui_instance
        cur_ui()

    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
