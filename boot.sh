#!/bin/bash 
cd /home/pi/pi-bot
modprobe cuse
uv4l --driver raspicam --auto-video_nr --width 320 --height 240 --encoding jpeg
