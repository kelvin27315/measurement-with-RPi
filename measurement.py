#!/usr/bin/env python

"""
温度を表示する
"""

from pathlib import Path
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import datetime as dt
import dht22, os, time

def get_data(pin):
    GPIO.setmode(GPIO.BCM)
    instance = dht22.DHT22(pin)
    while True:
        result = instance.read()
        if result.is_valid():
            GPIO.cleanup()
            return(result.temperature, result.humidity)
        time.sleep(6)

def measurement():
    temperature, humidity = get_data(17)
    print("湿度:\t{:.1f}%".format(humidity))
    print("温度:\t{:.1f}℃".format(temperature))
    tz = dt.timezone(dt.timedelta(hours=+9), "Asia/Tokyo")
    time = dt.datetime.now(tz).time()

    file_name = "{}.csv".format(dt.date.today())
    file_name = Path(__file__).parent.resolve() / "data" / file_name

    data = "\n{},{},{}".format(time.hour*60+time.minute, humidity, temperature)
    if os.path.isfile(file_name):
	    with open(file_name, "a") as f:
	        f.write(data)
    else:
	    with open(file_name, "w") as f:
	        f.write(",humidity,temperature{}".format(data))

def make_graph():
    #with open() as f:
    #    reader = csv.reader(f)
    plt.figure()
    plt.savefig(graph.png)

def main():
    measurement()
    #make_graph()

if __name__ == "__main__":
    main()
