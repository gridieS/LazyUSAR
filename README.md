# LazyUSAR

This service includes:

-   Automatic jumping jacks (No UI)

Planned to include:

-   Jumping jack assist (In development)
-   File automatic copy pasting (For tryouts, BCTs and more) (In development)
-   Smooth left & right faces (In development)

This project is currently in heavy development.

# Installation (Using binaries)

Coming soon..

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

Install the xdotool linux package (Should be already installed if you have x11 installed):

```bash
sudo apt install xdotool
```

or

```bash
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
