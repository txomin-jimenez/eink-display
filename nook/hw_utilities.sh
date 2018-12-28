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

enable_wifi()
{
        su -c 'svc wifi enable'
}

disable_wifi()
{
        su -c 'svc wifi disable'
}
