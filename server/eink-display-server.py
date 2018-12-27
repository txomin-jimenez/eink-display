from flask import Flask

import photo_frame

app = Flask(__name__)

photo_frame.init_app(app)