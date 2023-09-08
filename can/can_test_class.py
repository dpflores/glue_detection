from can_classes import *

CAN_INTERFACE = 'can0'
TRIGGER_IN_MESSAGE_ID = '0x260'
TRIGGER_OUT_MESSAGE_ID = '0x240'


def message_callback(cob_id, data, timestamp):
    print(data[0])


def main():
    can_red = CANOpen(CAN_INTERFACE)
    can_red.subscribe(TRIGGER_IN_MESSAGE_ID, message_callback)

    # Bucle para seguir ejecutando el programa
    while True:
        pass


if __name__ == '__main__':
    main()
