#!/usr/bin/env python

"""
温度を表示する
"""

from pathlib import Path
import matplotlib.pyplot as plt
#import RPi.GPIO as GPIO
import datetime as dt
import pandas as pd
#import dht22, os, time

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
    #print("湿度:\t{:.1f}%".format(humidity))
    #print("温度:\t{:.1f}℃".format(temperature))
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
    file_name = "{}.csv".format(dt.date.today())
    file_name = Path(__file__).parent.resolve() / "data" / file_name
    df = pd.read_csv(file_name, index_col=0)
    fig, ax = plt.subplots(2,1)
    fig.suptitle("Temperature and Humidity on the {}".format(dt.date.today()))
    ax[0].plot(df["temperature"], label="Temperature")
    ax[0].set_title("Temperature")
    ax[0].set_ylabel("temperature")
    ax[0].legend()
    ax[0].grid(True)
    #ax[0].set_yticklabels(["{}C".format(int(t)) if t.is_integer() else "{}C".format(t) for t in plt.yticks()[0]])

    ax[1].plot(df["humidity"], label="Humidity")
    ax[1].set_title("Humidity")
    ax[1].set_xlabel("time")
    ax[1].set_ylabel("humidity")
    ax[1].legend()
    ax[1].grid(True)
    label = ["{}:00".format(int(t/60)) if t%60 == 0 else "{}:{}".format(int(t/60),int(t%60)) for t in plt.xticks()[0]]
    ax[0].set_xticks(plt.xticks()[0])
    ax[0].set_xticklabels(label)
    ax[1].set_xticks(plt.xticks()[0])
    ax[1].set_xticklabels(label)
    ax[1].set_yticks(plt.yticks()[0])
    ax[1].set_yticklabels(["{}%".format(int(t)) if t.is_integer() else "{}%".format(t) for t in plt.yticks()[0]])
    fig.tight_layout()
    file_name = Path(__file__).parent.resolve() / "graph.png"
    plt.savefig(file_name)
    plt.close()

def main():
    #measurement()
    make_graph()

if __name__ == "__main__":
    main()
