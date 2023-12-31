from camera_classes import *
from can_classes import *

import cv2
import asyncio


import time

CAN_INTERFACE = 'can0'
TRIGGER_IN_MESSAGE_ID = '0x260'
TRIGGER_OUT_MESSAGE_ID = '0x240'


o3r = O3RCamera2D()
can_red = CANOpen(CAN_INTERFACE)

# Data para la detección de flanco
previus_state = 0


def analyze(image):
    print("Saving")
    cv2.imwrite('test_out.jpg', image)
    print("Saved")


def message_callback(cob_id, data, timestamp):
    global previus_state
    if data[0] == 1 and previus_state == 0:
        analyze(o3r.img)
    previus_state = data[0]


# code of the function message_callback2 that only saves the image if there is a rising edge


async def main():
    can_red.subscribe(TRIGGER_IN_MESSAGE_ID, message_callback)

    # La tomada de fotos se hace en un hilo aparte
    await o3r.run()

    # Bucle para seguir ejecutando el programa
    while True:
        can_red.send_high(TRIGGER_OUT_MESSAGE_ID)
        time.sleep(1)
        can_red.send_low(TRIGGER_OUT_MESSAGE_ID)
        time.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
