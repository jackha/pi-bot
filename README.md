pi-bot
======

Raspberry Pi based robot

Features::

- camera to look around
- pan/tilt servos
- more servos
- 16x2 display (NOT i2c)
- 8x8 pixels led display over i2c
- rotary encoders
- servos are controlled with the 16 channel pwm/servo driver from adafruit


Camera module
=============

Follow the guide on http://www.raspberrypi.org/camera

Make it stream video over the network

sudo apt-get install mplayer netcat


16x2 display
============

http://learn.adafruit.com/downloads/pdf/drive-a-16x2-lcd-directly-with-a-raspberry-pi.pdf

http://www.rpiblog.com/2012/11/interfacing-16x2-lcd-with-raspberry-pi.html


Configure RPi for I2C
=====================

http://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/configuring-your-pi-for-i2c



SimpleCV
========

https://github.com/sightmachine/SimpleCV/blob/develop/doc/HOWTO-Install%20on%20RaspberryPi.rst


Things to check
===============



http://tothinkornottothink.com/post/59305587476/raspberry-pi-simplecv-opencv-raspicam-csi-camera