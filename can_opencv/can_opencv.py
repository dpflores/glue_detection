from camera_classes import *
from can_classes import *

import cv2
import asyncio


import time

CAN_INTERFACE = 'can0'
TRIGGER_IN_MESSAGE_ID = '0x260'
TRIGGER_OUT_MESSAGE_ID = '0x240'


def message_callback(cob_id, data, timestamp):
    if data[0] == 1:
        cv2.imwrite('test.jpg', o3r.img)

    if data[0] == 0:
        print("No saving")


def main():
    can_red = CANOpen(CAN_INTERFACE)
    can_red.subscribe(TRIGGER_IN_MESSAGE_ID, message_callback)

    # Bucle para seguir ejecutando el programa
    while True:
        can_red.send_high(TRIGGER_OUT_MESSAGE_ID)
        time.sleep(1)
        can_red.send_low(TRIGGER_OUT_MESSAGE_ID)
        time.sleep(1)


if __name__ == '__main__':
    o3r = O3RCamera2D()
    asyncio.run(o3r.run())
    main()
