#!/bin/bash

# This script requires evtest and xdotool to be installed:
# sudo apt install evtest xdotool

# Load overlays for controlling rotary switch
# Rotary switch control is configured for GPIO 6 (pin 31) and GPIO 12 (pin 32).
sudo dtoverlay rotary-encoder pin_a=20 pin_b=16 relative_axis=1
# Pushbutton control is configured for GPIO 13 (pin 33)
sudo dtoverlay gpio-key gpio=21 label=MUTE keycode=113

sleep 2

# Get input device event names
rotaryswitch_input_device_event=$(readlink -f /dev/input/by-path/$(ls /dev/input/by-path | grep rotary))
pushbutton_input_device_event=$(readlink -f /dev/input/by-path/$(ls /dev/input/by-path | grep button))


# Rotary - volume control using OAP's global hotkey volume up and down functions
evtest $rotaryswitch_input_device_event |  \
    while read line ; do \
      if [[ $line =~ .*value\ 1.* ]]; then  \
          sh -c "xdotool key F8" /dev/null ;
      else  \
          if [[ $line =~ .*value\ -1.* ]]; then  \
              sh -c "xdotool key F7" > /dev/null ;
          fi; \
      fi; \
    done &

# Pushbutton - toggle mute / unmute
evtest $pushbutton_input_device_event |  \
    while read line ; do \
      if [[ $line =~ .*value\ 1.* ]]; then  \
          sh -c "amixer -q -D pulse sset Master toggle" > /dev/null ; \
      fi; \
    done