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
  'bc'

WORKDIR /tmp
RUN wget https://gitlab.com/wavexx/facedetect/-/archive/master/facedetect-master.zip
RUN unzip facedetect-master.zip
RUN cp facedetect-master/facedetect /usr/local/bin

WORKDIR /opt/eink-display
COPY . .

RUN pip3 install -r requirements.txt

CMD "./start_server.sh"
