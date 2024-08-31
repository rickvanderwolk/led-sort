#!/bin/bash

echo "Creating and activating a virtual environment (since pip cannot be used directly in newer versions of Raspberry Pi OS)..."
sudo apt install python3-venv -y

python3 -m venv led-sort
echo "Virtual environment 'led-sort' created."

source led-sort/bin/activate
echo "Virtual environment activated."

echo "Installing necessary libraries..."
pip install adafruit-blinka adafruit-circuitpython-neopixel Flask python-dotenv

echo "Copying and preparing the configuration file..."
cp led-sort/.env.example led-sort/.env
echo "Configuration file ready."

echo "Installation complete."
