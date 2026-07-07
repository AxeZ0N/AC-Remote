```markdown
A Python-based system that transmits 433 MHz OOK signals to control wireless RF outlets.  
Originally built to automatically shut down a modified 3D printer (Ender 3 V2) when idle, triggered by a Klipper G‑code macro.

---

## Features

- Transmits **433 MHz OOK** codes to commercial RF outlets.
- Pre‑programmed with the ON/OFF codes for **OUTLET_4** (used to power a 3D printer).
- Clean GPIO handling – resources are properly released on exit (Ctrl+C or script termination).
- A shell wrapper (`TOGGLE_OUTLET_4.sh`) that activates a Python virtual environment and runs the transmitter – ideal for calling from Klipper macros or cron jobs.

---

## Hardware Requirements

| Component | Purpose |
|-----------|---------|
| Raspberry Pi (any model) | Host computer |
| 433 MHz RF transmitter module (FS1000A or similar) | Sends OOK codes |
| Jumper wires | Connect transmitter to GPIO |
| 433 MHz RF receiver (optional) | Used during the original reverse‑engineering of outlet codes |

**GPIO Pin Mapping (default):**  
- RF transmitter data pin = **BCM 17**  

---

## Software Dependencies

- Python 3.6+
- `RPi.GPIO` (for GPIO control)
- `rpi-rf` (for sending/receiving 433 MHz OOK codes)

Install the required packages inside a virtual environment:

```bash
sudo apt install python3-venv python3-pip
python3 -m venv venv
source venv/bin/activate
pip install RPi.GPIO rpi-rf
```

---

## Setup

1. Navigate to the `RF_OUTLETS/` folder.
2. (Optional) Create and activate a virtual environment.
3. Ensure the transmitter is wired to **BCM pin 17** (or adjust the `TX_PIN` variable in `rf_remote.py`).
4. If you have captured codes for additional outlets, edit `rf_remote.py` and fill in the `OUTLET_X` dictionaries.

---

## Usage

### Manual Toggle

```bash
cd RF_OUTLETS
python3 rf_remote.py on   # Turn OUTLET_4 ON
python3 rf_remote.py off  # Turn OUTLET_4 OFF
```

### Using the Shell Wrapper

```bash
./TOGGLE_OUTLET_4.sh on
./TOGGLE_OUTLET_4.sh off
```

The shell script automatically activates the virtual environment before running the Python script.

### Klipper Integration (Auto‑Shutdown)

In your Klipper `printer.cfg`, define a G‑code macro that calls the shell script when a print completes or the printer becomes idle:

```ini
[gcode_macro SHUTDOWN_PRINTER]
gcode:
    RUN_SHELL_COMMAND CMD=shutdown_outlet

[shell_command shutdown_outlet]
command: /path/to/RF_OUTLETS/.TOGGLE_OUTLET_4.sh off
timeout: 10.
```

Then add `SHUTDOWN_PRINTER` to your end G‑code or invoke it manually.

---

## File Overview

- `rf_remote.py` – the main transmitter script, handles CLI arguments and transmits ON/OFF codes.
- `.TOGGLE_OUTLET_4.sh` – convenience shell wrapper for outlet 4 (includes venv activation).

---

## Background

The RF outlets were reverse‑engineered using an Arduino and a 433 MHz receiver, then the captured codes were ported to a Raspberry Pi for integration with a 3D printer running Klipper firmware.  
This system now automatically cuts power to the printer when not in use, reducing fire risk and energy waste.

---

*Part of the larger AC_Remote home‑automation project.*
```
