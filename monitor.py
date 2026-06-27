import time
import math
import board
import busio
import psycopg2
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

BURDEN_RESISTOR = 50.0       # burden resistor in ohms
CT_RATIO = 2000.0            # turn ratio of SCT-013-000
VOLTAGE_RMS = 120.0          # wall voltage 
noise_floor = .05			 # Base no load noise

#Need to set a connection the PostgreSQL to store the soon to be colleced data
conn = psycopg2.connect(
	dbname = "energy_monitor", 
	user = "postgres")
	
cursor = conn.cursor()


i2c = busio.I2C(board.SCL, board.SDA)	#configures microcontroller to gernerate I2C clocl signal on the SCL pin
ads = ADS.ADS1115(i2c)  				#initialize ADS1115
chan = AnalogIn(ads, 0)					#configures pin A0 on the ADS for input

#First need to read the voltage and calculate current, the return those values averaged over a thousand samples
def read_current(samples=1000):									#sets number of samples to 1000
    readings = []												#makes the list readings to collect voltage			

    for _ in range(samples):									
        readings.append(chan.voltage)							#adds another value to the readings list

    avg = sum(readings) / len(readings)							#averages the voltage values in the list

    voltage_rms = math.sqrt(
        sum((v - avg) ** 2 for v in readings) / len(readings)	#calculates the rms voltage
    )

    ct_secondary_current = voltage_rms / BURDEN_RESISTOR		#calculates the secondary current from the SCT
    primary_current = ct_secondary_current * CT_RATIO			#caulates the primary current from the SCT
	
	if primary_current < noise_floor:							
		primary_current = 0										#Ignores the current if it is less than the expected noise from no load
		
    return avg, voltage_rms, primary_current					#Returns the average voltage, rms voltage, and the current readings

#Stores the data into postgreSQL
cursor.execute(
	(bias, signal_vrms, current, power, energy_kwh))
	
	conn.commit()

while True:
    avg, signal_vrms, amps = read_current()						#Creates constants from the readings

    watts = amps * VOLTAGE_RMS									#Calculates power from load

    print(
        f"Bias: {avg:.3f} V | "									#prints bias voltage 
        f"Signal RMS: {signal_vrms:.4f} V | "					#prints signal rms voltage
        f"Current: {amps:.2f} A | "								#prints the rms current
        f"Power: {watts:.1f} W"									#prints the power
    )

    time.sleep(1)
