#!/usr/bin/env python3

import argparse
import signal
import sys
import time
import logging
import sys
import os

from rpi_rf import RFDevice

import RPi.GPIO

RPi.GPIO.setwarnings(False)

rfdevice = None

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s',)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# pylint: disable=unused-argument
def exithandler(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)

TX = True
RX = not TX

signal.signal(signal.SIGINT, exithandler)
TX_PIN = 17
RX_PIN = 27

if RX:
    rfdevice = RFDevice(RX_PIN)
    rfdevice.enable_rx()

if TX:
    rfdevice = RFDevice(TX_PIN, tx_pulselength=200)
    rfdevice.enable_tx()

timestamp = None

OUTLET_1 = { 'OFF' : None, 'ON' : None }
OUTLET_2 = { 'OFF' : None, 'ON' : None }
OUTLET_3 = { 'OFF' : None, 'ON' : None }
OUTLET_4 = { 'OFF' : 3093925, 'ON' : 3093933 }
OUTLET_5 = { 'OFF' : None, 'ON' : None }

while True:

    # testing_input  = ['foo', input('On or Off: ')]

    if len(sys.argv) > 1:
        if sys.argv[1].lower() == 'off' or sys.argv[1] == '0':
            rfdevice.tx_code(OUTLET_4['OFF'])
            logging.info(f'Repeating OFF signal of OUTLET_4: {OUTLET_4["OFF"]}')

        elif sys.argv[1].lower() == 'on' or sys.argv[1] == '1':
            rfdevice.tx_code(OUTLET_4['ON'])
            logging.info(f'Repeating ON signal of OUTLET_4: {OUTLET_4["ON"]}')

        [logging.info(f'{k,v}') for k,v in vars(rfdevice).items()]

    else:
        print('pass with on or off')
        os._exit(1)

    os._exit(0)

