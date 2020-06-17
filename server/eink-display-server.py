from datetime import datetime
from flask import Flask, redirect

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
