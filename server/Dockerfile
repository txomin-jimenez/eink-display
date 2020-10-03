FROM python:3.8-slim

RUN apt-get update
RUN apt-get install 'ffmpeg' \
  'libsm6' \
  'libxext6' -y \
  'git' \
  'wget' \
  'unzip' \
  'pngcrush' \
  'librsvg2-bin' \
  'imagemagick' \
  'bc' \
  'locales' \
  'cron'

RUN sed -i 's/^# *\(es_ES.UTF-8\)/\1/' /etc/locale.gen
RUN locale-gen

COPY ./weather/weather.cron /etc/cron.d/eink-weather
RUN chmod 0644 /etc/cron.d/eink-weather
RUN crontab /etc/cron.d/eink-weather
RUN touch /var/log/weatherjob.log

WORKDIR /tmp
RUN wget https://gitlab.com/wavexx/facedetect/-/archive/master/facedetect-master.zip
RUN unzip facedetect-master.zip
RUN cp facedetect-master/facedetect /usr/local/bin

WORKDIR /opt/eink-display
COPY . .

RUN pip3 install -r requirements.txt

CMD "./start_server.sh"
