# First Lego League Robot Controller (Pybricks)

This repository contains a small Pybricks-based control program for a LEGO Spike Prime robot. The workflow is designed so you can edit mission sequences as simple text files under `runs/`, then use a single script (`upload.sh`) to build a runnable program and send it to the hub over Bluetooth.

## Repository Structure

- `hemabot.py` — Robot setup and motion primitives (DriveBase, arm motors, command parser).
- `main.py` — UI and run-loop that selects and executes a mission from `run_data`.
- `runs/NN.txt` — Mission scripts (human-readable). Each line is a `CODE:VALUE` pair.
- `upload.sh` — Builder/uploader. Composes a temporary `_output.py` and runs it on the hub via BLE.

## How It Works

`upload.sh` generates a temporary `_output.py` with three parts, then runs it on the hub:

1) Import lines from `main.py`
- Command: `awk '/^from / || /^import /' main.py >> _output.py`
- Purpose: carry over any imports used by the UI loop (e.g., `Button`, `wait`).

2) Robot core from `hemabot.py`
- Appends the full `hemabot.py` so the robot class (`MetalMechRobot`) and the command executor are available.

3) Runtime data and the rest of `main.py`
- Builds `run_data` by reading and concatenating all `runs/*.txt` files (sorted). Newlines in each mission are converted to `#` so a mission becomes a single string. Double quotes are escaped.
- Appends everything in `main.py` that comes after the placeholder line `run_data = []` to wire up the UI and run loop against the generated `run_data`.

Finally, the script calls:

```
./upload.sh
```

This connects to the hub via Bluetooth, sends the generated program, and runs it immediately. The temporary file is then removed.

## Prerequisites

- Bash environment with standard UNIX tools: `awk`, `sed`, `tr`, `sort`.
- Python tooling: `pybricksdev` CLI.
  - Install: `pip install pybricksdev`
  - Verify: `pybricksdev --help`
- A LEGO Spike Prime (or equivalent Pybricks-compatible) hub with Bluetooth enabled.

## Usage

1) Add or edit missions under `runs/`:
   - Files like `runs/01.txt`, `runs/02.txt`, ... will be loaded and ordered alphabetically.
   - Each file is a list of `CODE:VALUE` lines (see “Mission Format” below).

2) Run the uploader:
   - Ensure the hub is powered on with Bluetooth available.
   - Execute `./upload.sh`
   - The script will build `_output.py`, upload it to the hub over BLE, run it, and delete the temporary file.

3) On the hub (runtime controls from `main.py`):
   - The display shows the currently selected mission index (1-based).
   - RIGHT button cycles to the next mission.
   - LEFT button confirms the selection and starts the mission.

## Mission Format (`runs/*.txt`)

Each mission file contains one command per line in the form `CODE:VALUE`. Units are chosen to be intuitive for Pybricks `DriveBase`:

- `SS`: straight speed in mm/s (e.g., `SS:700`)
- `SA`: straight acceleration in mm/s² (e.g., `SA:1000`)
- `ST`: turn (angular) speed in deg/s (e.g., `ST:750`)
- `TA`: turn (angular) acceleration in deg/s² (e.g., `TA:900`)
- `AS`: arm motor speed in deg/s (e.g., `AS:700`)
- `F`: forward distance in cm (the code multiplies by 10 to get mm)
- `B`: backward distance in cm (multiplied by 10 to get mm)
- `L`: left turn in degrees (positive value)
- `R`: right turn in degrees (positive value)
- `PR`: point turn using right wheel only (degrees)
- `PL`: point turn using left wheel only (degrees)
- `LA`: left auxiliary arm motor rotate (degrees)
- `RA`: right auxiliary arm motor rotate (degrees)
- `AA`: rotate both arm motors together. Accepts one or two values:
  - `AA:X` rotates both arms by `X` degrees.
  - `AA:L:R` rotates left by `L` and right by `R` degrees.
- `W`: wait in seconds

Example (`runs/01.txt`):

```
SS:700
SA:1000
ST:750
TA:900
AS:700
RA:-29
F:64
L:125
```

Additional `AA` examples:

```
AS:600
AA:90        # both arms +90°
AA:90:-45    # left +90°, right -45°
```
