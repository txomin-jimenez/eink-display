#!/system/bin/sh

press_lock_button(){
        sendevent /dev/input/event1 0001 0116 00000001
        sendevent /dev/input/event1 0000 0000 00000000
        sendevent /dev/input/event1 0001 0116 00000000
        sendevent /dev/input/event1 0000 0000 00000000
}

get_screen_state(){
  state=`dumpsys power | grep 'mPowerState=' | tail -n 1`
  if [ "$state" = "  mPowerState=" ]; then
        echo "off"
  else
        echo "on"
  fi
}

sleep_device(){
        screen_state=$(get_screen_state)
        if [ "$screen_state" = "on" ]; then
                press_lock_button
        fi
}

wake_device() {
        screen_state=$(get_screen_state)
        if [ "$screen_state" = "off" ]; then
                press_lock_button
        fi
}

su -c 'svc wifi enable'
sleep 10
# download and update lock image
wget -O /media/screensavers/photo_frame/weather.png http://server/weather/weather.png;
su -c 'svc wifi disable'
# refresh screen for getting new lock image
wake_device
sleep 1
sleep_device
