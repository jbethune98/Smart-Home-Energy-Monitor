import csv
from datetime import datetime

def log_data(current, power):

    with open("data.csv", "a", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            datetime.now(),
            round(current, 3),
            round(power, 2)
        ])
