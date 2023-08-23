import time
import cv2
from ifm3dpy import O3R
from ifm3dpy import FrameGrabber, buffer_id
import datetime

counter = 0


def callback(self):
    global counter
    counter += 1
    print("callback called: ", counter)
    rgb = cv2.imdecode(self.get_buffer(
        buffer_id.JPEG_IMAGE), cv2.IMREAD_UNCHANGED)

    cv2.imwrite(
        'captures2/capture_{}.png'.format(counter), rgb)
    cv2.imshow("2D image", rgb)
    cv2.waitKey(1)


# Initialize the objects
o3r = O3R()
port = "port0"
fg = FrameGrabber(o3r, pcic_port=50010)

# Change port to RUN state
config = o3r.get()
config["ports"][port]["state"] = "RUN"
o3r.set(config)

# Register a callback and start streaming frames
fg.on_new_frame(callback)
fg.start([buffer_id.JPEG_IMAGE])

time.sleep(10)
# Stop the streaming
fg.stop()
