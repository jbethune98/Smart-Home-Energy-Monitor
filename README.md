# Smart-Home-Energy-Monitor
This system will monitor the power consumption and provide real time data visualization using a raspberry pi and a current sensor.
A non-invasive current transformer (CT) clamp such as an SCT-013 Current Transformer will connect power to an ADC(analog to digital converter), as the pi lacks the ability to read analog signals. The ADC will then be connected to the pi which will use python code to read the measurments and log them to a csv file.
Once measured the data will stored in InfluxDB, and visualized with Grafana, displaying Current power draw, Daily energy usage, Historical trends, and Estimated cost
Ideally also sends messages when certain spikes occur, or when certain high power appliances are turned on.
