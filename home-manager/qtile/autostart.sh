#!/bin/sh
xrandr --output 'DP-4' --mode 1920x1080 --primary --rate 144.00
xrandr --output 'DP-1' --mode 1920x1080 --rate 144.00 --right-of 'DP-4'
xrandr --output 'HDMI-0' --mode 1920x1080 --rate 60.00 --left-of 'DP-4'
picom -b &
dunst &
lxpolkit &
