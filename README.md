# LED sort

![LED-strip](IMG_0458.png)

A Python (Raspberry Pi) script that visualizes various sorting algorithms on a LED strip. Changing the LED colors to represent the sorting progress: green for correctly placed values, red for incorrect positions, and purple for each swap. It uses a Flask web server to display the current algorithm's name and the iteration count while cycling through different sorting methods like Bubble Sort, Quick Sort, Pancake Sort, etc.

- [Hardware](#hardware)
- [Getting started](#getting-started)
- [Run script](#run-script)
- [View webpage](#view-webpage)

<a id="hardware"></a>
## Hardware

- Raspberry Pi; I use a Pi Zero WH but any Pi will probably do just fine
- LED strip; I use a cheap WS2812B LED strip from Aliexpress. You can use any strip as long as it has individually addressable RGB LEDs and is compatible with the `adafruit-circuitpython-neopixel` library.
- Power supply for the Pi
- Power supply for the LED strip; Depending on the type of LED strip and the desired brightness it is probably a good idea to use a separate power supply for the LED strip

<a id="#getting-started"></a>
## Getting started

## Install

1. Install Raspberry Pi OS on a SD card. You can easily choose the right image and setup a username / password, Wi-Fi and enable SSH with the [Raspberry Pi OS imager](https://www.raspberrypi.com/software/). I've used the latest recommended image `Raspberry Pi OS (32-bit) - Release date 2024-07-04 - A port of Debian Bookworm with the Raspberry Pi Desktop` in the example below, but I recommend just installing the latest recommended version.
2. Boot the Pi (might take a while depending on which Pi you're using)
3. Connect via SSH `ssh <your-pi-username>@<your-pi-ip>`
4. Clone repository `git clone https://github.com/rickvanderwolk/led-sort.git`
5. In newer versions of Raspberry Pi OS we can not use `pip` (Python package manager) directly. We can use a virtual environment by installing `sudo apt install python3-venv`
6. Create a virtual environment `python -m venv led-sort`
7. Activate virtual environment `source led-sort/bin/activate`
8. Install necessary libraries `pip install adafruit-blinka adafruit-circuitpython-neopixel Flask`
9. Connect LED strip data pin to the Raspberry Pi via `GPIO 18`
10. If needed, change number of LEDs `NUMBER_OF_LEDS` (default 60) and / or `BRIGHTNESS` (default 0.5) with `nano led-sort/main.py`. Press `ctrl` + `x` and then `y` to save
11. [Run script](#run-script)

### Start script on boot (optional)

1. `crontab -e`
2. Choose nano by pressing `1` + `enter`
3. Add to following line `@reboot sleep 30 && sudo led-sort/bin/python led-sort/main.py >> /home/piledsort/led-sort/cron.log 2>&1`
4. Press `ctrl` + `x` and then `y` to save
5. Reboot `sudo reboot`

<a id="#run-script"></a>
## Run script

Run script `sudo led-sort/bin/python led-sort/main.py`. You probably need to use `sudo` to run the script as we use the GPIO pins for communication with the LED strip.

<a id="#view-webpage"></a>
## View webpage

Visit `http://<your-pi-ip>:5000`
