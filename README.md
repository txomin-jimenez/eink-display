Intro
-----

Modified version of [Matthew Petroff's script](http://www.mpetroff.net/archives/2012/09/14/kindle-weather-display/) to display current weather information on an e-ink screen.

Here is an example of it running a Nook Somple Touch

![nook](http://i.imgur.com/uSXlJ3Q.jpg "Nook weather")

(note that running it on a Nook requires the companion [WeatherShow](https://github.com/zeronickname/WeatherShow) android app -- or well, anything that can display png's really)

Changes (from MPetroff's version)
-------

* Uses forecast.io for the weather information (original script used NOAA data and was US only)
* Switched to using icons from [The Noun Project](http://thenounproject.com/collections/weather-icons/)
* Minor mods to the actual information displayed (timestamp, human redable weather info)


Pre-Requisites
--------------
* [forecast.io API key](https://developer.forecast.io/)
* [python-forecastio](https://github.com/ZeevG/python-forcast.io)
* rsvg-convert to convert the svg to a png (sudo apt-get install librsvg2-bin)
* pngcrush to optimize/reduce the final image filesize (sudo apt-get install pngcrush)

Inctructions for use
--------------------

TBD
