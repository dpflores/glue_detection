from ifm3dpy import O3R, FrameGrabber, buffer_id
import cv2
import argparse
import asyncio
import datetime
import json
import numpy as np
import os


CAMERA_IP = '192.168.0.69'
XMLRPC_PORT = 80
PCIC_PORT = 50010


ports_dict = {"50010": "port0", "50011":"port1", "50012":"port2", "50013":"port3", "50014":"port4", "50015":"port5"}


# Here we implement a class called O3R that implements viewer.py in order to simplify the code


class O3RCamera2D:
    def __init__(self, ip=CAMERA_IP, xmlrpc_port=XMLRPC_PORT, pcic_port=PCIC_PORT):
        self.ip = ip
        self.cam = O3R(ip, xmlrpc_port)
        self.getter = self.get_jpeg
        self.pcic_port = pcic_port
        self.port = ports_dict[str(pcic_port)]
        self.activate_camera()
        path = os.path.dirname(os.path.abspath(__file__))
        self.img = cv2.imread(path + '/test.png')

    def activate_camera(self, rate=15):
        config = self.cam.get()  # get the configuration saved on the VPU
        # Expecting a head on Port
        config['ports'][self.port]['acquisition']['framerate'] = rate
        config['ports'][self.port]['state'] = "RUN"  # Expecting a head on Port

        self.cam.set(config)

    def get_jpeg(self, frame):
        return cv2.imdecode(frame.get_buffer(buffer_id.JPEG_IMAGE), cv2.IMREAD_UNCHANGED)

    async def display_2d(self, fg, getter, title):
        fg.start([buffer_id.NORM_AMPLITUDE_IMAGE, buffer_id.RADIAL_DISTANCE_IMAGE,
                  buffer_id.XYZ, buffer_id.REFLECTIVITY, buffer_id.MONOCHROM_2D])

        cv2.startWindowThread()

        cv2.namedWindow(title, cv2.WINDOW_NORMAL)

        while True:
            self.frame = await fg.wait_for_frame()

            self.img = getter(self.frame)
            if self.img is not None:
                cv2.imshow(title, self.img)

                cv2.waitKey(15)

                if cv2.getWindowProperty(title, cv2.WND_PROP_VISIBLE) < 1:
                    break

        cv2.destroyAllWindows()

    async def get_2d(self, fg, getter, title):

        while True:
            self.frame = await fg.wait_for_frame()
            self.img = getter(self.frame)
            # print(self.img)

    async def run_display(self):
        # Esto se puede probar en la computadora conectada al OVP pues es con visualización
        fg = FrameGrabber(self.cam, pcic_port=self.pcic_port)
        fg.start()
        title = "O3R Port {}".format(str(self.pcic_port))
        await self.display_2d(fg, self.getter, title)
        return self.img

    async def run(self):
        # Esto es sin visualización
        fg = FrameGrabber(self.cam, pcic_port=self.pcic_port)
        fg.start()
        title = "O3R Port {}".format(str(self.pcic_port))
        await self.get_2d(fg, self.getter, title)
        return self.img


# For testing purposes
if __name__ == "__main__":
    o3r = O3RCamera2D()
    asyncio.run(o3r.run())
