import time
import math
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, 0)

while True:
    readings = []

    for i in range(1000):
        readings.append(chan.voltage)

    v_min = min(readings)
    v_max = max(readings)
    v_avg = sum(readings) / len(readings)

    print(
        "Avg:", round(v_avg, 3),
        "Min:", round(v_min, 3),
        "Max:", round(v_max, 3),
        "Peak-to-peak:", round(v_max - v_min, 3)
    )

    time.sleep(1)
