
"""
Pure calculation functions for the Smart Energy Monitor.

This module contains the mathematical parts of the project only.
It does not communicate with the Raspberry Pi, ADS1115, SCT-013,
or PostgreSQL database.

Keeping calculations separate makes them easy to test because the
functions can use pretend sample data instead of real sensor hardware.
"""

import math


def calculate_signal_rms(readings):
    """
    Calculate the DC bias voltage and AC RMS voltage of sensor samples.

    The SCT-013 signal is biased around approximately 1.65 V because
    the ADS1115 cannot measure negative voltages. For example, a current
    waveform may move above and below 1.65 V instead of moving above
    and below 0 V.

    This function:
    1. Finds the average voltage, which is the DC bias.
    2. Subtracts that bias from each sample.
    3. Calculates the RMS value of the remaining AC waveform.

    Args:
        readings (list[float]): Voltage samples read from the ADS1115.

    Returns:
        tuple[float, float]:
            bias_voltage: Average voltage of all samples in volts.
            signal_vrms: RMS voltage of the AC signal in volts.

    Raises:
        ValueError: If no readings are provided.
    """
    # A calculation cannot be performed without at least one sample.
    if not readings:
        raise ValueError("At least one voltage reading is required.")

    # The average of the readings represents the DC bias voltage.
    # In this project, it should normally be close to 1.65 V.
    bias_voltage = sum(readings) / len(readings)

    # Remove the DC bias from each reading, square each AC value,
    # find their average, then take the square root.
    #
    # This is the RMS formula:
    # RMS = sqrt(sum(sample^2) / number_of_samples)
    signal_vrms = math.sqrt(
        sum((voltage - bias_voltage) ** 2 for voltage in readings)
        / len(readings)
    )

    return bias_voltage, signal_vrms


def calculate_current(signal_vrms, burden_resistor, ct_ratio, noise_floor):
    """
    Convert measured SCT signal voltage into estimated primary current.

    The ADS1115 measures voltage across the burden resistor. Ohm's Law
    converts that voltage into CT secondary current:

        secondary_current = voltage / resistance

    The SCT-013 current transformer ratio then converts secondary current
    into the estimated current in the wire being measured.

    Args:
        signal_vrms (float): RMS voltage from the SCT signal in volts.
        burden_resistor (float): Burden resistor value in ohms.
        ct_ratio (float): Current transformer ratio of the SCT sensor.
        noise_floor (float): Minimum valid current in amps.

    Returns:
        float: Estimated RMS primary current in amps.

    Raises:
        ValueError: If burden_resistor is zero or negative.
        ValueError: If ct_ratio is zero or negative.
    """
    # Dividing by zero would cause an error and would not make
    # physical sense for a burden resistor.
    if burden_resistor <= 0:
        raise ValueError("Burden resistor must be greater than zero.")

    # A CT ratio must be positive because it represents a physical ratio.
    if ct_ratio <= 0:
        raise ValueError("CT ratio must be greater than zero.")

    # Use Ohm's Law to calculate the current through the burden resistor.
    secondary_current = signal_vrms / burden_resistor

    # Scale the CT secondary current to estimate current in the monitored wire.
    primary_current = secondary_current * ct_ratio

    # Small values can come from ADC noise, electrical interference,
    # or tiny fluctuations in the bias circuit. Treat values below the
    # configured threshold as zero current.
    if primary_current < noise_floor:
        return 0.0

    return primary_current


def calculate_power(current_amps, voltage_rms):
    """
    Estimate electrical power from RMS current and RMS voltage.

    This uses the simplified formula:

        power = current × voltage

    This estimate is most accurate for resistive loads such as heaters,
    toasters, incandescent bulbs, and hair dryers. It does not account
    for power factor, so it is less accurate for motors and electronics.

    Args:
        current_amps (float): RMS current in amps.
        voltage_rms (float): Assumed line voltage in volts.

    Returns:
        float: Estimated electrical power in watts.
    """
    return current_amps * voltage_rms


def update_energy_kwh(current_energy_kwh, power_watts, elapsed_seconds):
    """
    Add energy used during a time interval to the running kWh total.

    Power is measured in watts and time is measured in seconds.
    There are 3,600,000 watt-seconds in one kilowatt-hour:

        1 kWh = 1000 watts × 3600 seconds
              = 3,600,000 watt-seconds

    Args:
        current_energy_kwh (float): Existing energy total in kWh.
        power_watts (float): Power used during the interval in watts.
        elapsed_seconds (float): Length of the interval in seconds.

    Returns:
        float: Updated accumulated energy total in kWh.

    Raises:
        ValueError: If elapsed_seconds is negative.
    """
    # Negative elapsed time would mean time moved backward, which should
    # not happen during normal monitor operation.
    if elapsed_seconds < 0:
        raise ValueError("Elapsed time cannot be negative.")

    # Convert watt-seconds to kilowatt-hours and add it to the total.
    energy_used_kwh = (power_watts * elapsed_seconds) / 3_600_000

    return current_energy_kwh + energy_used_kwh
