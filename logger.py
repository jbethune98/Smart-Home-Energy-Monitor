"""
Database logging functions.

This module contains functions for writing energy monitor
measurements to the PostgreSQL database.
"""

def save_reading(cursor, conn, bias, signal_vrms, current, power, energy_kwh):
    """
    Save a single energy measurement to the PostgreSQL database.

    Args:
        cursor: Active PostgreSQL database cursor.
        conn: Active PostgreSQL database connection.
        bias (float): Average ADC bias voltage.
        signal_vrms (float): RMS voltage of the AC signal.
        current (float): Calculated RMS current in amps.
        power (float): Calculated power in watts.
        energy_kwh (float): Accumulated energy consumption in kilowatt-hours.
    """

    # Execute a parameterized SQL query to safely insert the
    # latest sensor reading into the database.
    cursor.execute(
        """
        INSERT INTO readings
        (bias_voltage, signal_rms, current, power, energy)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (bias, signal_vrms, current, power, energy_kwh)
    )

    # Commit the transaction so the new record is permanently
    # written to the database.
    conn.commit()
