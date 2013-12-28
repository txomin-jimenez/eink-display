from time import gmtime, strftime
import forecastio
import textwrap
import codecs

def main():



    api_key = "YOUR_FORECAST.IO_API_KEY"
    lat = 51.477
    lng = 0.0000

    forecast = forecastio.load_forecast(api_key, lat, lng)
    by_day = forecast.daily()

    # Open SVG to process
    output = codecs.open('weather-script-preprocess.svg', 'r', encoding='utf-8').read()

    # Insert icons and temperatures
    output = output.replace('ICON_ONE',by_day.data[0].icon).replace('ICON_TWO',by_day.data[1].icon).replace('ICON_THREE',by_day.data[2].icon).replace('ICON_FOUR',by_day.data[3].icon)
    output = output.replace('HIGH_ONE',str(int(round(by_day.data[0].temperatureMax)))).replace('HIGH_TWO',str(int(round(by_day.data[1].temperatureMax)))).replace('HIGH_THREE',str(int(round(by_day.data[2].temperatureMax)))).replace('HIGH_FOUR',str(int(round(by_day.data[3].temperatureMax))))
    output = output.replace('LOW_ONE',str(int(round(by_day.data[0].temperatureMin)))).replace('LOW_TWO',str(int(round(by_day.data[1].temperatureMin)))).replace('LOW_THREE',str(int(round(by_day.data[2].temperatureMin)))).replace('LOW_FOUR',str(int(round(by_day.data[3].temperatureMin))))

    #insert summary of day text
    summary=textwrap.wrap(forecast.hourly().summary,55)

    wrappedsummary = summary[0]

    # the pre-process svg file has space for three lines of text. ANy more and we cut it off
    if len(summary) > 1  :
        wrappedsummary = wrappedsummary + '<tspan x="25" dy="25">' + summary[1] + '</tspan>'
        if len(summary) > 2  :
            wrappedsummary = wrappedsummary + '<tspan x="25" dy="25">' + summary[2] + '</tspan>'
        

    output = output.replace('TODAY_SUMMARY',wrappedsummary)

    # Insert days of week
    output = output.replace('DAY_THREE',by_day.data[2].time.strftime('%A')).replace('DAY_FOUR',by_day.data[3].time.strftime('%A'))

    #Insert timestamp
    output = output.replace('DATE_TIME', strftime("%H:%M %d/%m", gmtime()))

    # Write output
    codecs.open('weather-script-output.svg', 'w', encoding='utf-8').write(output)


if __name__ == "__main__":
    main()
