```markdown
# 3D Printer RF Outlet Automation

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

# AC Remote – Servo Button Presser

A Raspberry Pi‑based automation script that physically presses the power button of an infrared air‑conditioner remote using a micro servo.  
No modification to the remote’s internal circuitry is required – the servo simply pushes the existing button.

---

## Features

- **Physical button press** – rotates a servo to press and release the remote’s power button.
- Adjustable angles to match the exact travel distance of your remote.
- Two versions provided: an interactive script (`my_servo.py`) that waits for user input, and a simpler test script (`press_button.py`).

---

## Hardware Requirements

| Component | Purpose |
|-----------|---------|
| Raspberry Pi (any model with GPIO) | Host computer |
| Micro servo (e.g. SG90) | Presses the remote button |
| Jumper wires | Connect servo to GPIO |
| External 5V power supply (recommended) | Powers the servo without overloading the Pi |

**GPIO Pin Mapping (default):**  
- Servo signal wire = **BCM pin 3**

---

## Software Dependencies

- Python 3.6+
- `RPi.GPIO` (for PWM servo control)

Install with:

```bash
sudo apt install python3-pip
pip install RPi.GPIO
```

---

## Setup

1. Place the servo so that its horn can press the AC remote’s power button cleanly.
2. Wire the servo:
   - Signal → BCM pin 3
   - Power → external 5V (or Pi’s 5V pin if the servo draws little current – external supply is safer)
   - Ground → common ground with the Pi
3. Test the angles by editing `my_servo.py` or `press_button.py` and running with:

```bash
sudo python3 my_servo.py
```

---

## Usage

### Interactive Control

```bash
sudo python3 my_servo.py
```

- The servo initialises and waits for you to press **Enter**.
- Pressing Enter rotates the servo to 90°, then to 135° (presses button), then returns.
- Adjust the `setAngle()` calls inside the script if your remote needs a different travel.

### Simple Test

```bash
sudo python3 press_button.py
```

- Similar behaviour but uses a slightly different PWM approach; also waits for Enter before each press.

---

## Customisation

- Change the servo angles in `setAngle(angle)` – the default sequence is 90° → 135°.
- The pulse width range (`SERVO_MIN_PULSE` / `SERVO_MAX_PULSE`) can be tuned for your specific servo model.

---

## Background

This project was created to automate a wall‑unit air conditioner that only responds to infrared signals. Instead of building an IR blaster, a small servo physically presses the remote’s button on command, integrating the AC into a larger home‑automation workflow driven by a Raspberry Pi.

---

*Part of the larger AC_Remote home‑automation project.*
```
