#include <sensor.py>
#include <calculations.py>
#include <logger.py>
from sensor import get_samples
from calculations import rms, estimate_power
from logger import log_data

while True:

    samples = get_samples()

    current = rms(samples)

    power = estimate_power(current)

    print(
        f"Current: {current:.2f} A | "
        f"Power: {power:.2f} W"
    )

    log_data(current, power)

    import time
    time.sleep(1)
