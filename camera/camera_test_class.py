from camera_classes import *
# Here we implement a class called O3R that implements viewer.py in order to simplify the code


# For testing purposes
if __name__ == "__main__":
    o3r = O3RCamera2D()
    asyncio.run(o3r.run())
