import codecs
from datetime import datetime
from flask import Flask, redirect
import subprocess

import photo_frame
import weather

HEARTBEAT_FILE = 'heartbeat'

app = Flask(__name__)

# init app modules
photo_frame.init_app(app)
weather.init_app(app)

# main
@app.route('/e-ink-display')
def display_image():
  write_heartbeat()
  return redirect(get_display_module())

def get_display_module():
  now = datetime.now()
  if now.minute >= 30:
    return "/photo_frame"
  else:
    return "/weather"

def write_heartbeat():
    with open(HEARTBEAT_FILE, 'w') as file:
        heartbeat_data = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        file.write(heartbeat_data)

@app.errorhandler(404)
def page_not_found(e):
  print(e)
  output = build_error_response('ERROR', 'Resource not found')
  return output, 404, {'Content-Type': 'image/png'}

@app.errorhandler(500)
def internal_error(e):
  print(e)
  output = build_error_response('ERROR', 'Internal Server Error')
  return output, 500, {'Content-Type': 'image/png'}

def build_error_response(error_title, error_message_1, error_message_2 = ''):
  output = codecs.open("warning.svg", 'r', encoding='utf-8').read()
  output = output.replace('#LINE_1', error_title)
  output = output.replace('#LINE_2', error_message_1)
  output = output.replace('#LINE_3', error_message_2)
  codecs.open('/tmp/warning.svg', 'w', encoding='utf-8').write(output)
  shell_run(f"rsvg-convert --background-color=white -o /tmp/warning.png /tmp/warning.svg")
  shell_run(f"pngcrush -c 0 -ow /tmp/warning.png")

  return open("/tmp/warning.png", 'rb').read()

def shell_run(command):
    output = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True
    )
    stdout, stderr = output.communicate()
    if stderr is not None:
        raise RuntimeError(f"Shell command failed: {stderr}")

    return stdout.decode("utf-8")
