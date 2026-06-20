import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Start I2C connection
i2c = busio.I2C(board.SCL, board.SDA)

# Create ADS1115 object
ads = ADS.ADS1115(i2c)

# Read from A0
chan = AnalogIn(ads, 0)

while True:
    print("Voltage:", round(chan.voltage, 3), "V")
    time.sleep(1)
