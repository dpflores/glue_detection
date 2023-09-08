
import canopen
import os

OVP_ID = 123


def send_high():
    print('sending high')
    id_str = '0x240'
    id = int(id_str, 16)
    nw.send_message(id, bx01, remote=False)


def send_low():
    print('sending low')
    id_str = '0x240'
    id = int(id_str, 16)
    nw.send_message(id, bx00, remote=False)


def on_message_received(cob_id, data, timestamp):
    # Log the received message
    # print("Received message: cob_id={}, data={}, timestamp={}".format(cob_id, data, timestamp))

    # guardar en variable si es que la entrada del primer byte es 1 o 0

    if data[0] == 1:
        # print("HIGH")
        pass
    if data[0] == 0:
        # print("LOW")
        pass


nw = canopen.Network()
nw.connect(bustype="socketcan", channel="can0")

id_str = '0x260'
id = int(id_str, 16)
listener = nw.subscribe(id, on_message_received)


# Keep the program running to receive messages
while True:
    # para ejecutar la funcion send_high y send_low cuando se reciba las teclas w y s de la terminal
    key = input("Enter a key: ")
    if key == "w":
        send_high()
    elif key == "s":
        send_low()
    else:
        print("Invalid key, please enter a valid key.")
