from flask import send_from_directory

WEATHER_OUTPUT_FOLDER = './www/weather'

def init_app(app):
  @app.route('/weather')
  def show_weather():
    filename = 'weather.png'
    return send_from_directory(WEATHER_OUTPUT_FOLDER, filename)

