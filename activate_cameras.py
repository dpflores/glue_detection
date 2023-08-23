import json
from ifm3dpy import O3R
o3r = O3R()
config = o3r.get()  # get the configuration saved on the VPU

# print(config)


config['ports']['port0']['state'] = "RUN"  # Expecting a head on Port 0
# config['ports']['port1']['state'] = "RUN" #Expecting a head on Port 0
# config['ports']['port2']['state'] = "RUN"  # Expecting a head on Port 0
# config['ports']['port3']['state'] = "RUN" #Expecting a head on Port 0
o3r.set(config)
print(json.dumps(config, indent=4))
# o3r.set(config)


# #print(config)


# from ifm3dpy import FrameGrabber, buffer_id
# import matplotlib.pyplot as plt


# fg = FrameGrabber(o3r, pcic_port=50012) #Expecting a head on Port 0 (Port 0 == 50010)
# im = buffer_id()
# #print(help(ImageBuffer()))
# #print(im.distance_image())
# if fg.wait_for_frame(im, 1000):
#     print(im.xyz_image().shape)
#     plt.imshow(im.xyz_image())
#     plt.colorbar()

# plt.show()
