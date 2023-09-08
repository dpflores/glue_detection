
import canopen


def on_message_received(cob_id, data, timestamp):
    # Log the received message
    print("Received message: cob_id={}, data={}, timestamp={}".format(
        cob_id, data, timestamp))


nw = canopen.Network()
nw.connect(bustype="socketcan", channel="can0")

# Prompt the user for a CAN ID to subscribe to
while True:
    try:
        id_str = input(
            "Enter a CAN ID to subscribe to (in hex format, e.g. 0x123): ")
        id = int(id_str, 16)
        break
    except ValueError:
        print("Invalid input, please enter a valid hex number.")

listener = nw.subscribe(id, on_message_received)

# Keep the program running to receive messages
while True:
    pass

# nw.send_message(123, bx00x113x88x88D, remote=False)
