from flask import Flask
from flask import redirect
from flask import render_template
from flask import url_for

from hifi.constants import CONTROLS

app = Flask(__name__)


@app.route('/')
def remote_controller():
    return render_template('remote_controller.html', controls=CONTROLS)


@app.route('/action/<int:key>')
def action(key):
    # TODO: perform action
    return redirect(url_for('remote_controller'))


if __name__ == '__main__':
    app.run()
