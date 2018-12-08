#!/bin/sh

cd "$(dirname "$0")"

python weather-script.py
rsvg-convert --background-color=white -o weather-script-output.png weather-script-output.svg
pngcrush -c 0 -ow weather-script-output.png weather.png
# cp -f weather.png /media/usbhdd1tb/others/weather_display/weather.png
