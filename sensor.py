"""
Sensor interface for the smart energy monitor.

This file communicates with the ADS1115 over I2C and converts
the SCT-013 voltage waveform into RMS current.
"""

import math
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from config import burden_resistor, ct_ratio, noise_floor

# Inititalize the Raspberry Pi I2C bus and ADS1115 ADC
i2c = busio.I2C(board.SCL, board.SDA)
ads1115 = ADS.ADS1115(i2c)

# The SCT-013 signal is connected to ADS channel A0
chan = AnalogIn(ads1115, 0)

def read_current(samples=1000):
    """
    Read the SCT-013 current sensor.

    Collects a number of voltage samples from the ADS1115,
    removes the DC bias, calculates the RMS voltage of the AC
    waveform, and converts it into RMS current.

    Args:
        samples (int): Number of ADC samples to collect.

    Returns:
        tuple:
            bias (float): Average DC bias voltage.
            signal_vrms (float): RMS voltage of the AC waveform.
            primary_current (float): Estimated RMS current in amps.
    """
    readings = []
	
	# Collect voltage samples from the ADS1115
    for _ in range(samples):
        readings.append(chan.voltage)

    # DC bias, should be around 1.65 V
    bias = sum(readings) / len(readings)

    # Remove bias and calculate AC RMS voltage
    signal_vrms = math.sqrt(
        sum((v - bias) ** 2 for v in readings) / len(readings)
    )

    # Convert the measured RMS voltage across the burden resistor
    #into the CT secondary current, then scale it to the primary current.
    ct_secondary_current = signal_vrms / burden_resistor
    primary_current = ct_secondary_current * ct_ratio

    # Ignore very small currents caused by electrical noise and ADC jitter
    if primary_current < noise_floor:
        primary_current = 0.0

    return bias, signal_vrms, primary_current
