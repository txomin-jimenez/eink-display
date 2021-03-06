from datetime import datetime
import os
import time
from urllib import request, parse
from pytz import timezone, utc

WAIT_INTERVAL = 1800
HEARTBEAT_FILE = 'heartbeat'

def main():
    log("Running....")
    while True:
        last_hearbeat = get_last_heartbeat()
        current_datetime = datetime.utcnow()
        difference = current_datetime - last_hearbeat
        if difference.seconds > WAIT_INTERVAL:
            notify_nook_disconnected(last_hearbeat)
        log("Wait " + str(WAIT_INTERVAL) + " seconds until next check...")
        time.sleep(WAIT_INTERVAL)

def notify_nook_disconnected(last_hearbeat):
    if is_time_to_not_disturb():
        log("DND hours. do not notify")
        return

    log("notify nook is disconnected...")
    bot = os.environ['NOTIFY_BOT']
    token = os.environ['NOTIFY_TOKEN']
    chat_id = os.environ['NOTIFY_CHATID']
    url = "https://api.telegram.org/" + bot + ":" + token + "/sendMessage"
    message = {
        "chat_id": chat_id,
        "text": "🔋 Se ha perdido la conexion con el marco de fotos desde " + localize_utc_date(last_hearbeat) + ". Toca recargarlo 🔌"
    }
    data = parse.urlencode(message).encode()
    req =  request.Request(url, data=data)
    resp = request.urlopen(req)

def is_time_to_not_disturb():
    now = datetime.now()
    return now.hour >= 21 or now.hour <= 8

def localize_utc_date(utc_timestamp):
    LOCAL_TZ = timezone('Europe/Madrid')
    UTC = utc
    return UTC.localize(utc_timestamp).astimezone(LOCAL_TZ).strftime('%Y-%m-%d %H:%M:%S.%f')

def get_last_heartbeat():
    try:
        with open(HEARTBEAT_FILE) as file:
            heartbeat_data = file.read().split('\n')[0]

        return datetime.strptime(heartbeat_data, '%Y-%m-%d %H:%M:%S.%f')
    except FileNotFoundError:
        return datetime.utcnow()

def log(message):
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    print('[' + now + '] - ' + message)

if __name__ == "__main__":
    main()
