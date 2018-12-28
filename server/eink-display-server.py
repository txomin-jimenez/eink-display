from flask import Flask

import photo_frame
import weather

app = Flask(__name__)

photo_frame.init_app(app)
weather.init_app(app)