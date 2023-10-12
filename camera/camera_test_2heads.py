import threading


import time


from camera_classes import *


CAMERA_IP = '192.168.0.69'
XMLRPC_PORT = 80

o3r0 = O3RCamera2D(ip=CAMERA_IP, xmlrpc_port=XMLRPC_PORT, pcic_port=50010)
o3r1 = O3RCamera2D(ip=CAMERA_IP, xmlrpc_port=XMLRPC_PORT, pcic_port=50011)


async def camera0():
    await o3r0.run_display()
async def camera1():
    await o3r1.run_display()


async def main():
    await asyncio.gather(camera0(), camera1())


asyncio.run(main())
