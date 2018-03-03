from flask import Flask
from flask import redirect
from flask import render_template
from flask import url_for

from constants import CONTROLS
from serial_communicator import SerialCommunicator

app = Flask(__name__)


@app.route('/')
def remote_controller():
    return render_template('remote_controller.html', controls=CONTROLS)


@app.route('/send_command/<command>')
def send_command(command):
    SerialCommunicator.send_command(command)
    return redirect(url_for('remote_controller'))


if __name__ == '__main__':
    app.run()
