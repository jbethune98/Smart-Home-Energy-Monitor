import time
import math
import board
import busio

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# ADS1115 setup
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

# Read from A0
chan = AnalogIn(ads, ADS.P0)

while True:

    samples = []

    # Collect samples
    for _ in range(1000):
        samples.append(chan.voltage)

    # Find DC offset (bias voltage)
    offset = sum(samples) / len(samples)

    # Remove offset
    ac = [x - offset for x in samples]

    # RMS voltage at ADC input
    rms_voltage = math.sqrt(
        sum(v*v for v in ac) / len(ac)
    )

    print(
        f"Offset={offset:.3f}V "
        f"RMS={rms_voltage:.4f}V"
    )

    time.sleep(1)
