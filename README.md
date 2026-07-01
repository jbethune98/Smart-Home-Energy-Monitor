# Smart-Home-Energy-Monitor

Status:
  Functional prototype with automated calculation tests and hardware smoke testing 
  Calibrated against a known load giving <1% error.  

Database logging Validation: 
  Ran the energy monitor continuously for apporiximately 21 minutes
  Confirmed that 118 timestaps where stored, giving and average logging interval of 11 seconds
  Verified that the database recored measurments consistently throughout the testing period.


This system will monitor the power consumption and provide real time data visualization using a raspberry pi and a current sensor.
A non-invasive current transformer (CT) clamp such as an SCT-013 Current Transformer will connect power to an ADC(analog to digital converter), as the pi lacks the ability to read analog signals. The ADC will then be connected to the pi which will use python code to read the measurments and store them in PostgreSQL. 
After Storing the data in PostgreSQL, Grafana will be used to visualize the data, displaying Current power draw, Daily energy usage, Historical trends, and Estimated cost
Ideally also sends messages when certain spikes occur, or when certain high power appliances are turned on.
