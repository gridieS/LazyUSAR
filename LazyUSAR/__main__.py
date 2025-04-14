from . import jumping_jacks, ui


def main():
    try:
        jumping_jacks_ui = ui.JumpingJackUI(
            "f6",
            "f5",
        )
        jumping_jacks_ui.start()

    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
