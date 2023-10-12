from camera_classes import *


CAMERA_IP = '192.168.0.69'
XMLRPC_PORT = 80



# For testing purposes
if __name__ == "__main__":
    # Camera 0
    o3r0 = O3RCamera2D(ip=CAMERA_IP, xmlrpc_port=XMLRPC_PORT, pcic_port=50010)
    asyncio.run(o3r0.run_display())

    # Camera 1
    o3r1 = O3RCamera2D(ip=CAMERA_IP, xmlrpc_port=XMLRPC_PORT, pcic_port=50011)
    asyncio.run(o3r1.run_display())