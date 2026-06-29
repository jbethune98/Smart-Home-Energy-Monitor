"""
Database connection test.

This script verifies that the Raspberry Pi can successfully
connect to the PostgreSQL database using the project
credentials. It is intended to be run once during setup
or troubleshooting.
"""

import psycopg2

from config import db_host, db_name, db_user, db_password

def connect_database():
    # Attempt to establish a connection to the local PostgreSQL server.
    conn = psycopg2.connect(
        host="localhost",
        database="energy_monitor",
        user="energy_user",
        password="energy123"
    )
    cursor = conn.cursor()
    return conn, cursor
