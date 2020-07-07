from datetime import datetime
import os
import time
from urllib import request, parse
from pytz import timezone, utc

WAIT_INTERVAL = 1800
HEARTBEAT_FILE = 'heartbeat'

def main():
    print("Running....")
    while True:
        last_hearbeat = get_last_heartbeat()
        current_datetime = datetime.utcnow()
        difference = current_datetime - last_hearbeat
        if difference.seconds > WAIT_INTERVAL:
            notify_nook_disconnected(last_hearbeat)
        print("Wait " + WAIT_INTERVAL + " seconds until next check...")
        time.sleep(WAIT_INTERVAL)

def notify_nook_disconnected(last_hearbeat):
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


if __name__ == "__main__":
    main()
