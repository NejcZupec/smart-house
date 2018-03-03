import os

from flask import current_app
import serial


class SerialCommunicator(object):
    """ Singleton class for serial communication

    Establish a serial connection only once, because the initialization of a
    serial connection is very slow.
    """

    _instance = None

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

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = \
                super(SerialCommunicator, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        serial_name = self._figure_out_serial_name()
        self.serial_connection = serial.Serial(serial_name) \
            if serial_name else None
        if self.serial_connection:
            msg = 'Serial connection was established. ' \
                  'Used serial port: {}'.format(serial_name)
            current_app.logger.info(msg)
        else:
            msg = 'Serial connection was not established. Plugin the ' \
                  'device via USB.'
            current_app.logger.info(msg)

    @staticmethod
    def _figure_out_serial_name():
        devices = os.listdir('/dev/')
        usb_devices = [file_ for file_ in devices if 'ttyUSB' in file_]

        try:
            device_name = usb_devices[0]
        except IndexError:
            msg = 'USB serial not found. The remote controller won\'t work.'
            current_app.logger.warn(msg)
            return

        return '/dev/' + device_name

    def send_command(self, command):
        """ Send a command via a serial USB connection

        Args:
            command [string]: one of commands listed in the COMMANDS constant
        """
        if not self.serial_connection:
            msg = 'Can\'t sent a command via serial. The connection was ' \
                  'not established.'
            current_app.logger.error(msg)
            return

        action_key = self.COMMANDS[command]
        self.serial_connection.write(action_key)

        # volume commands should be sent multiple times to increase the impact
        if command in ['volume_up', 'volume_down']:
            for _ in range(30):
                self.serial_connection.write(action_key)
        msg = 'Command {} with key {} was sent'.format(command, action_key)
        current_app.logger.info(msg)
