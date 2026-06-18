import math

##takes the current and finds the average 
def rms(samples):
	mean_square = sum(x*x for x in samples)/ len(samples)
	return math.sqrt(mean_square)
	
def estimate_power(current_rms, voltage=120):
	return current_rms * voltage
