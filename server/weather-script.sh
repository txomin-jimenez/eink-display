#!/bin/bash

cd "$(dirname "$0")"

python weather-script.py
rsvg-convert --background-color=white -o weather-script-output.png weather-script-output.svg
pngcrush -c 0 -ow weather-script-output.png
cp -f weather-script-output.png /var/www/html/weather/weather.png
