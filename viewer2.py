#!/usr/bin/env python3

# # SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2020 ifm electronic gmbh
#
# THE PROGRAM IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.
#

from ifm3dpy import O3R, FrameGrabber, buffer_id
import cv2
import argparse
import asyncio
import datetime

try:
    import open3d as o3d
    OPEN3D_AVAILABLE = True
except ModuleNotFoundError:
    OPEN3D_AVAILABLE = False


# VARIABLES
# El threshold es el valor que se usa para binarizar la imagen (0 - 255)
THRESHOLD = 100
# Tamaño de la ventana del filtro gaussiano
GAUSSIAN_WINDOW_SIZE = 7

img = cv2.imread('images/rellena_not_filled_close.png')


def get_jpeg(frame):
    return cv2.imdecode(frame.get_buffer(buffer_id.JPEG_IMAGE), cv2.IMREAD_UNCHANGED)


def get_distance(frame):
    img = cv2.normalize(frame.get_buffer(buffer_id.RADIAL_DISTANCE_IMAGE), None, 0,
                        255, cv2.NORM_MINMAX, cv2.CV_8U)
    img = cv2.applyColorMap(img, cv2.COLORMAP_JET)
    return img


def get_amplitude(frame):
    # print(frame.get_buffer(buffer_id.NORM_AMPLITUDE_IMAGE).shape)
    return frame.get_buffer(buffer_id.NORM_AMPLITUDE_IMAGE)


def get_reflectivity(frame):
    # print(frame.get_buffer(buffer_id.NORM_AMPLITUDE_IMAGE).shape)
    return frame.get_buffer(buffer_id.REFLECTIVITY)


def get_mono(frame):
    # print(frame.get_buffer(buffer_id.NORM_AMPLITUDE_IMAGE).shape)
    return frame.get_buffer(buffer_id.MONOCHROM_2D)


def get_xyz(frame):
    return frame.get_buffer(buffer_id.XYZ)


async def display_2d(fg, getter, title):
    fg.start([buffer_id.NORM_AMPLITUDE_IMAGE, buffer_id.RADIAL_DISTANCE_IMAGE,
             buffer_id.XYZ, buffer_id.REFLECTIVITY, buffer_id.MONOCHROM_2D])
    cv2.startWindowThread()
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    while True:
        frame = await fg.wait_for_frame()

        img = getter(frame)

        # grayscale image
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Gaussian filter of the image with kernel of 5x5
        img2 = cv2.GaussianBlur(
            img2, (GAUSSIAN_WINDOW_SIZE, GAUSSIAN_WINDOW_SIZE), 0)

        # thresholding the image
        ret, img3 = cv2.threshold(img2, THRESHOLD, 255, cv2.THRESH_BINARY)

        # resize images img2 and img3 TO 500x500
        img2 = cv2.resize(img2, (500, 500))
        img3 = cv2.resize(img3, (500, 500))
        cv2.imshow(title, img)
        cv2.imshow('Gray', img2)
        cv2.imshow('Thresh', img3)
        # cv2.waitKey(15)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite(
                'captures/capture_{}.png'.format(str(datetime.datetime.now())), img)

        if cv2.getWindowProperty(title, cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()


async def display_3d(fg, getter, title):
    fg.start([buffer_id.NORM_AMPLITUDE_IMAGE,
             buffer_id.RADIAL_DISTANCE_IMAGE, buffer_id.XYZ])
    vis = o3d.visualization.Visualizer()
    vis.create_window(title)

    first = True
    while True:
        frame = await fg.wait_for_frame()

        img = getter(frame)

        img = img.reshape(img.shape[0]*img.shape[1], 3)
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(img)

        vis.clear_geometries()
        vis.add_geometry(pcd, first)
        if not vis.poll_events():
            break

        vis.update_renderer()

        first = False

    vis.destroy_window()


async def main():
    image_choices = ["jpeg", "distance", "amplitude", "reflectivity", "mono"]
    if OPEN3D_AVAILABLE:
        image_choices += ["xyz"]

    parser = argparse.ArgumentParser()
    parser.add_argument("--pcic-port", help="The pcic port from which images should be received", type=int,
                        required=False, default=50010)
    parser.add_argument("--image", help="The image to received (default: distance)", type=str,
                        choices=image_choices, required=False, default="jpeg")
    parser.add_argument("--ip", help="IP address of the sensor (default: 192.168.0.69)",
                        type=str, required=False, default="192.168.0.69")
    parser.add_argument("--xmlrpc-port", help="XMLRPC port of the sensor (default: 80)",
                        type=int, required=False, default=80)
    args = parser.parse_args()

    getter = globals()["get_" + args.image]

    cam = O3R(args.ip, args.xmlrpc_port)
    fg = FrameGrabber(cam, pcic_port=args.pcic_port)
    fg.start()
    title = "O3R Port {}".format(str(args.pcic_port))

    if args.image == "xyz":
        await display_3d(fg, getter, title)
    else:
        await display_2d(fg, getter, title)


if __name__ == "__main__":

    asyncio.run(main())
