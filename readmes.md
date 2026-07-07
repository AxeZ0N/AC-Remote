```markdown
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
