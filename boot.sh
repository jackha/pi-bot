#!/bin/bash 
cd /home/pi/pi-bot
modprobe cuse
uv4l --driver raspicam --auto-video_nr --width 640 --height 480 --encoding jpeg
