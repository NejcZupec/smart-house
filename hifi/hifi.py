import logging
import sys

from flask import Flask
from flask import redirect
from flask import render_template
from flask import url_for

from constants import CONTROLS
from serial_communicator import SerialCommunicator


def _setup_logging(app_):
    """ Set logging

    Based on this blog post:
    http://y.tsutsumi.io/global-logging-with-flask.html
    """

    handler = logging.StreamHandler(sys.stdout)

    # set format
    fmt = '%(asctime)s [%(levelname)s][%(module)s] %(message)s'
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)

    # add handler
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    app_.logger.handlers = []
    app_.logger.propagate = True


def _create_app():
    app_ = Flask(__name__)
    _setup_logging(app_)
    return app_


app = _create_app()


@app.route('/')
def remote_controller():
    return render_template('remote_controller.html', controls=CONTROLS)


@app.route('/send_command/<command>')
def send_command(command):
    communicator = SerialCommunicator()
    communicator.send_command(command)
    return redirect(url_for('remote_controller'))


if __name__ == '__main__':
    SerialCommunicator()  # establish a connection
    app.run()
