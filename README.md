# LazyUSAR

This service includes:

-   Automatic jumping jacks (UI)
-   File automatic copy pasting (For tryouts, BCTs and more)

Plans abandoned:

-   Jumping jack assist

# Installation (Using binaries)

NOTE: All binaries are in the x86_64 architecture.

## Windows

Download the LazyUSAR.exe file from the latest release, and double click on it in the file manager to run, it's that simple!

## Linux

Download the LazyUSAR.bin file from the latest release, and then add the execute permission on the file using

```bash
chmod +x LazyUSAR.bin
```

Then, simply execute the file with

```bash
./LazyUSAR.bin
```

# Installation (Using python)

## Windows

Create and activate a virtual enviroment using python3's venv module:

```cmd
py -m venv .venv
.venv/Scripts/activate.bat
```

Or with powershell:

```powershell
py -m venv .venv
.venv/Scripts/activate.ps1
```

Install the package requirements:

```cmd
pip install -r requirements-windows.txt
```

Then simply run the package:

```cmd
py -m LazyUSAR
```

## Linux

Install the xdotool and tkinter linux package (Should be already installed if you have x11 and python installed):

```bash
sudo apt install python3-tk
sudo apt install xdotool
```

or

```bash
sudo dnf install python3-tkinter
sudo dnf install xdotool
```

Create and activate a virtual enviroment using python3's venv module:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the package requirements

```bash
pip install -r requirements-linux.txt
```

Then run the package keeping python's virtual enviroment:

```bash
sudo env PATH=$PATH python3 -m LazyUSAR
```

# Usage

Upon running the package, you are shown a UI made with python's Tkinter.

The package is forcefully exited on the key press F6.

You can change the options as you like, and then you can press the run button/F5 to start the listener.

You are first shown the Jumping Jack Controller UI, used for modifying the Jumping Jack controller's options. You may press the switch button at the bottom of the UI for switching to the Script Playback UI.

## Jumping Jack Controller Listener Keybinds

The listener listens for three keyboard keys: "j", "k", and "l":

-   k is used for starting/stopping the jumping jacks
-   j is used for setting the jumping jack value to the previous value
-   l is used for setting the jumping jack value to the next value

## Script Playback Controller Listener Keybinds

The listener listens for the same three keyboard keys: "j", "k", and "l":

-   k is used for starting/stopping the playback
-   j is used for setting the line index value to the previous value
-   l is used for setting the line index value to the next value

## Script Playback Usage

You may open a text file, or paste your script into a textbox.

Every entry of \<username\> and \<name\> gets replaced by the value you set in the UI.

Every entry of \<rank\> also gets replaced by the value you set in the UI.
