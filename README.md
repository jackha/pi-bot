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


Raspbian
========

Install raspbian wheezy. Do not forget to 'unlock' the free space::

    $ sudo raspi-config

16x2 display
============

http://learn.adafruit.com/downloads/pdf/drive-a-16x2-lcd-directly-with-a-raspberry-pi.pdf


    $ sudo apt-get install python-dev
    $ sudo apt-get install python-setuptools
    $ sudo easy_install -U distribute
    $ sudo apt-get install python-pip
    $ sudo pip install rpi.gpio

to see if it works::


    $ sudo python Adafruit_CharLCD.py


http://www.rpiblog.com/2012/11/interfacing-16x2-lcd-with-raspberry-pi.html


Configure RPi for I2C
=====================

http://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/configuring-your-pi-for-i2c



Camera / SimpleCV / OpenCV
==========================

Follow the guide on http://www.raspberrypi.org/camera


Make camera work in SimpleCV::

http://www.linux-projects.org/modules/sections/index.php?op=viewarticle&artid=14

OpenCV and SimpleCV::
    $ wget https://raw.github.com/jayrambhia/Install-OpenCV/master/Ubuntu/2.4/opencv2_4_6_1.sh
    $ chmod +x opencv2_4_6_1.sh
    $ ./opencv2_4_6_1.sh

    $ sudo apt-get install git
    $ git clone git://github.com/sightmachine/SimpleCV.git
    $ cd SimpleCV
    $ python setup.py install


    $ sudo modprobe cuse
    $ pi@raspberrypi ~ $ uv4l --driver raspicam --auto-video_nr --width 640 --height 480 --encoding jpeg

Copy boot.sh to /boot (NOT symlink!)::

    $ sudo cp boot.sh /boot

Add in /etc/rc.local::

/boot/boot.sh


Additionally::

    $ sudo pip install svgwrite


More info::


https://github.com/sightmachine/simplecv

https://github.com/sightmachine/SimpleCV/blob/develop/doc/HOWTO-Install%20on%20RaspberryPi.rst

http://tothinkornottothink.com/post/59305587476/raspberry-pi-simplecv-opencv-raspicam-csi-camera


Things to check
===============



http://tothinkornottothink.com/post/59305587476/raspberry-pi-simplecv-opencv-raspicam-csi-camera