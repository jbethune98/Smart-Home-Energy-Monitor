import time
import math
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

BURDEN_RESISTOR = 50.0       # ohms
CT_RATIO = 2000.0            # SCT-013-000: 100A / 0.05A = 2000
VOLTAGE_RMS = 120.0          # wall voltage estimate

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, 0)

def read_current(samples=1000):
    readings = []

    for _ in range(samples):
        readings.append(chan.voltage)

    avg = sum(readings) / len(readings)

    voltage_rms = math.sqrt(
        sum((v - avg) ** 2 for v in readings) / len(readings)
    )

    ct_secondary_current = voltage_rms / BURDEN_RESISTOR
    primary_current = ct_secondary_current * CT_RATIO

    return avg, voltage_rms, primary_current

while True:
    avg, signal_vrms, amps = read_current()

    watts = amps * VOLTAGE_RMS

    print(
        f"Bias: {avg:.3f} V | "
        f"Signal RMS: {signal_vrms:.4f} V | "
        f"Current: {amps:.2f} A | "
        f"Power: {watts:.1f} W"
    )

    time.sleep(1)
