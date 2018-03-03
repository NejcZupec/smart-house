import os
from time import sleep
import sys

import serial

commands = {
    'on': b'0',
    'volume_down': b'1',
    'volume_up': b'2',
    'mute': b'3',
    'channel_dvd': b'4',
    'channel_tv': b'5',
    'channel_game': b'6',
    'channel_mp3': b'7',
}


def figure_out_serial():
    devs = os.listdir('/dev/')
    try:
        device_name = [file_ for file_ in devs if 'ttyUSB' in file_][0]
    except IndexError:
        print("USB serial not found")
        return
    return '/dev/' + device_name


def main():
    key = sys.argv[1]
    if not key:
        print('key was not specified. The command was not sent.')
        return

    serial_name = figure_out_serial()
    print('Serial name: {}'.format(serial_name))

    ser = serial.Serial(serial_name)

    command = commands[key]
    sleep(2)
    ser.write(command)
    if command in ['volume_up', 'volume_down']:
        for _ in xrange(30):
            ser.write(command)
    print('Command "{}" was sent to Hi-Fi system.'.format(key))
    ser.close()

main()
