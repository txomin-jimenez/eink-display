Eink display
------------

Small utility for serving images to be displayed on e-ink devices such as Nook Simple Touch.
This allows to reuse this devices as photo frames or dashboard for information that updates regularly.

For more information on the original inspiration see [the original blog post](http://www.mpetroff.net/archives/2012/09/14/kindle-weather-display/).

Code is split in two pieces:
  * Server: to be deployed in a Raspberry PI for example.
  * Nook: client script for getting display updates from server.

Server
--------

Server is a small Python Flask app for serving display image in a single endpoint.
This endpoint has a schedule that switches between photo frame and weather forecast module every 30 minutes.

* **Weather forecast module**

  Weather code script originally designed by [mpetroff](https://github.com/mpetroff/kindle-weather-display), modified by [zeronickname](https://github.com/zeronickname/kindle-weather-display) before ending up here. Changes (from zeronickname's version):

  * Refactored server script into smaller pieces.
  * Show weather forecast using spanish language
  * Localize timestamps because I had issues with timezones

  `weather-script.sh` must be scheduled using cron inside server. Python API will only serve updated image at this time.

  ![nook](https://i.imgur.com/CGwU3L3.png "Nook weather")

* **Photo frame**
  * Photo gallery folder
  * Random image from gallery is served
  * Photo upload form
  * Uploads via POST
  * Special addition for uploading photos with iOS shortcuts.
  * Photos are converted to 600x800 greyscale portrait images
  * Face recognition to properly crop landscape images taking people into account
  * Auto improve image levels


Nook
----

This requires a rooted Nook device with cron or a old version of Tasker for scheduling the script.


Pre-Requisites
--------------
* Python 3
* [forecast.io API key](https://developer.forecast.io/)
* [python-forecastio](https://github.com/ZeevG/python-forcast.io)
* rsvg-convert to convert the svg to a png (sudo apt-get install librsvg2-bin)
* pngcrush to optimize/reduce the final image filesize (sudo apt-get install pngcrush)
* ImageMagick
* [Facedetect](https://github.com/wavexx/facedetect)
* [OpenCV](https://life2coding.com/install-opencv-3-4-0-python-3-raspberry-pi-3)

Usage
-----

Server development:
```
$ cd server
$ pip3 install -r requirements.txt
$ flask run
```

Useful link for deploying production server with Gunicorn: [link](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux)
