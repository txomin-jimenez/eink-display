#!/system/bin/sh
. hw_utilities.sh

enable_wifi
sleep 10
# download and update lock image
wget -O /media/screensavers/e-ink-display/image.png http://server:port/e-ink-display;
disable_wifi
# refresh screen for getting new lock image
wake_device
sleep 1
sleep_device
