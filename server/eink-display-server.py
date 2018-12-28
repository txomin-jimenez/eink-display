from datetime import datetime
from flask import Flask, redirect

import photo_frame
import weather

app = Flask(__name__)

# init app modules
photo_frame.init_app(app)
weather.init_app(app)

# main
@app.route('/e-ink-display')
def display_image():
  return redirect(get_display_module())

def get_display_module():
  now = datetime.now()
  if now.minute >= 30:
    return "/photo_frame"
  else:
    return "/weather"