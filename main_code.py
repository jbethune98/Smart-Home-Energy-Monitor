import time
from config import voltage_rms
from sensor import read_current
from database import connect_database
from logger import save_reading

"""
Main program for the smart energy monitor.

This file coordinates the full system:
1. Connects to PostgreSQL.
2. Reads current from the SCT-013 sensor.
3. Calculates power and accumulated energy.
4. Saves each reading to the database.
5. Prints live measurements to the terminal.
"""

def main():
    """
    Run the main energy monitor loop.

    The loop continuously reads current data from the sensor,
    estimates power, accumulates total energy in kWh, stores
    the reading in PostgreSQL, and prints the live values.
    """
    conn, cursor = connect_database()

    energy_kwh = 0.0
    last_time = time.time()

    print("Smart Energy Monitor started.")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            now = time.time()
            
            # Measure elapsed time so energy can be accumulated correctly.
            elapsed = now - last_time
            last_time = now

            # Read current from SCT sensor
            bias, signal_vrms, current = read_current()

            # Convert current to estimated real power using assumed wall voltage.
            power = current * voltage_rms

            # Accumulate energy over time
            energy_kwh += (power * elapsed) / 3600000

            # Save reading to database
            save_reading(cursor, conn, bias, signal_vrms, current, power, energy_kwh)

            # Print live values
            print(
                f"Bias: {bias:.3f} V | "
                f"Signal RMS: {signal_vrms:.4f} V | "
                f"Current: {current:.2f} A | "
                f"Power: {power:.1f} W | "
                f"Energy: {energy_kwh:.6f} kWh"
            )

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping monitor.")

    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()
