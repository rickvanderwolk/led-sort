# create and activate a virtual environment as we can not use `pip` directly in newer versions of Raspberry Pi OS
sudo apt install python3-venv
python -m venv led-sort
source led-sort/bin/activate
# install necessary libraries
pip install adafruit-blinka adafruit-circuitpython-neopixel Flask python-dotenv
# copy / prepare config
cp led-sort/.env.example led-sort/.env
