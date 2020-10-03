from datetime import datetime
from time import strftime
from tzlocal import get_localzone
from pytz import timezone
import codecs
import forecastio
import locale
import os
import pytz
import textwrap

TIME_LANG = "es_ES.UTF-8"
UTC = pytz.utc
LOCAL_TZ = timezone('Europe/Madrid')

def main():
    locale.setlocale(locale.LC_TIME, TIME_LANG)

    forecastio_api_key = os.environ['FORECASTIO_API_KEY']

    forecast = WeatherForecast(forecastio_api_key)

    ImageBuilder(forecast).build().save()

def localize_utc_date(utc_timestamp):
    return UTC.localize(utc_timestamp).astimezone(LOCAL_TZ)

class WeatherForecast:
    lat = 43.2
    lng = -2.077222
    language = "es"

    def __init__(self, api_key):
        self.api_key = api_key
        self.forecast = forecastio.load_forecast(self.api_key, self.lat, self.lng, lang=self.language)

    def today_summary(self):
        summary = textwrap.wrap(self.forecast.hourly().summary, 55)
        return self.__wrap_summary(summary)

    def daily(self):
        forecast_by_day = self.forecast.daily()
        return list(map(lambda day_data: WeatherForecast.Day(day_data), forecast_by_day.data))

    def __wrap_summary(self, summary):
        wrappedsummary = summary[0]
        # the pre-process svg file has space for three lines of text. ANy more and we cut it off
        if len(summary) > 1  :
            wrappedsummary = wrappedsummary + '<tspan x="25" dy="25">' + summary[1] + '</tspan>'
            if len(summary) > 2  :
                wrappedsummary = wrappedsummary + '<tspan x="25" dy="25">' + summary[2] + '</tspan>'

        return wrappedsummary

    class Day:
        def __init__(self, forecast):
            self.forecast = forecast

        def label(self):
            return localize_utc_date(self.forecast.time).strftime('%A').capitalize()

        def icon(self):
            return self.forecast.icon

        def temperatureMax(self):
            return str(int(round(self.forecast.temperatureMax)))

        def temperatureMin(self):
            return str(int(round(self.forecast.temperatureMin)))

class ImageBuilder:
    template_file = 'weather-script-preprocess.svg'
    output_file = 'weather-script-output.svg'

    def __init__(self, forecast):
        # Open SVG to process
        self.template = codecs.open(self.template_file, 'r', encoding='utf-8').read()
        self.output = self.template

        self.forecast = forecast
        forecast_by_day = forecast.daily()

        self.today_forecast = forecast_by_day[0]
        self.tomorrow_forecast = forecast_by_day[1]
        self.day_three_forecast = forecast_by_day[2]
        self.day_four_forecast = forecast_by_day[3]

    def build(self):
        self.__build_today_summary()
        self.__build_weekday_labels()
        self.__build_icons()
        self.__build_max_temperatures()
        self.__build_min_temperatures()
        self.__build_current_timestamp()
        return self

    def save(self):
        codecs.open(self.output_file, 'w', encoding='utf-8').write(self.output)

    def replace_content(self, template_key, content):
        self.output = self.output.replace(template_key, content)

    def __build_today_summary(self):
        summary = self.forecast.today_summary()
        self.replace_content('TODAY_SUMMARY', summary)

    def __build_weekday_labels(self):
        self.replace_content('DAY_THREE', self.day_three_forecast.label())
        self.replace_content('DAY_FOUR', self.day_four_forecast.label())

    def __build_icons(self):
        self.replace_content('ICON_ONE', self.today_forecast.icon())
        self.replace_content('ICON_TWO', self.tomorrow_forecast.icon())
        self.replace_content('ICON_THREE', self.day_three_forecast.icon())
        self.replace_content('ICON_FOUR', self.day_four_forecast.icon())

    def __build_max_temperatures(self):
        self.replace_content('HIGH_ONE', self.today_forecast.temperatureMax())
        self.replace_content('HIGH_TWO', self.tomorrow_forecast.temperatureMax())
        self.replace_content('HIGH_THREE', self.day_three_forecast.temperatureMax())
        self.replace_content('HIGH_FOUR', self.day_four_forecast.temperatureMax())

    def __build_min_temperatures(self):
        self.replace_content('LOW_ONE', self.today_forecast.temperatureMin())
        self.replace_content('LOW_TWO', self.tomorrow_forecast.temperatureMin())
        self.replace_content('LOW_THREE', self.day_three_forecast.temperatureMin())
        self.replace_content('LOW_FOUR', self.day_four_forecast.temperatureMin())

    def __build_current_timestamp(self):
        timestamp = localize_utc_date(datetime.utcnow()).strftime("%H:%M %d/%m")
        self.replace_content('DATE_TIME', timestamp)


if __name__ == "__main__":
    main()
