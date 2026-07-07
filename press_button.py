import RPi.GPIO as GPIO
from time import sleep

SERVO_MIN_PULSE = 500
SERVO_MAX_PULSE = 2500
ServoPin = 3

if __name__ == '__main__':     #Program start from here
    try:
        GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by BCM
        GPIO.setup(ServoPin, GPIO.OUT)   # Set ServoPin's mode is output
        GPIO.output(ServoPin, GPIO.LOW)  # Set ServoPin to low
        p = GPIO.PWM(ServoPin, 50)     # set Frequecy to 50Hz

        while True:
            p.start(50)
            p.stop()
            input('Enter to press button')
            p.ChangeDutyCycle(5)
            sleep(1)
            print('Rotations complete')

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the program destroy() will be executed.
        p.stop()
        GPIO.cleanup()

