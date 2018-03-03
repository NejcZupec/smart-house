import os
from time import sleep

from flask import current_app
import serial


class SerialCommunicator(object):

    # a mapper between commands and action keys accepted by the remote
    COMMANDS = {
        'on': b'0',
        'volume_down': b'1',
        'volume_up': b'2',
        'mute': b'3',
        'channel_dvd': b'4',
        'channel_tv': b'5',
        'channel_game': b'6',
        'channel_mp3': b'7',
    }

    @staticmethod
    def _figure_out_serial():
        devices = os.listdir('/dev/')

        usb_devices = [file_ for file_ in devices if 'ttyUSB' in file_]

        try:
            device_name = usb_devices[0]
        except IndexError:
            current_app.logger.warn('USB serial not found')
            return

        return '/dev/' + device_name

    @classmethod
    def send_command(cls, command):
        """ Send a command via a serial USB connection
        Args:
            command [string]: one of commands listed in the COMMANDS constant
        """
        serial_name = cls._figure_out_serial()

        if not serial_name:
            current_app.logger.error('Can\'t sent a command via serial')
            return

        current_app.logger.info('Serial name: {}'.format(serial_name))

        ser = serial.Serial(serial_name)
        sleep(2)

        action_key = cls.COMMANDS[command]

        ser.write(action_key)
        if command in ['volume_up', 'volume_down']:
            for _ in range(30):
                ser.write(action_key)
        msg = 'Command {} with key {} was sent'.format(command, action_key)
        current_app.logger.info(msg)
        ser.close()
