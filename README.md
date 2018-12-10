Intro
-----

For more information on the orignal inspiration see [the original blog post](http://www.mpetroff.net/archives/2012/09/14/kindle-weather-display/).

Code originally designed by [mpetroff](https://github.com/mpetroff/kindle-weather-display), modified by [zeronickname](https://github.com/zeronickname/kindle-weather-display) before ending up here.

Server script is running on a Raspberry PI 1.
Nook script is scheduled in Nook device using and old version of Tasker.

![nook](https://i.imgur.com/CGwU3L3.png "Nook weather")

Changes (from zeronickname's version)
-------

* Refactored server script into smaller pieces.
* Show weather forecast using spanish language
* Localize timestamps because I had issues with timezones
* A new script for Nook device that updates lock image and refreshes device screen.

Pre-Requisites
--------------
* [forecast.io API key](https://developer.forecast.io/)
* [python-forecastio](https://github.com/ZeevG/python-forcast.io)
* rsvg-convert to convert the svg to a png (sudo apt-get install librsvg2-bin)
* pngcrush to optimize/reduce the final image filesize (sudo apt-get install pngcrush)

