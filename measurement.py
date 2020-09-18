#!/usr/bin/env python

from pathlib import Path
from board import D17
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
import adafruit_dht, os, time

class Measurement():
    def __init__(self):
        self.path = Path(__file__).parent.resolve()
        self.today = dt.date.today()
        self.yesterday = self.today - dt.timedelta(days=1)

    def get_csv_file_name(self, day):
        return(self.path / "data" / "{}.csv".format(day))

    def measurement(self):
        d = adafruit_dht.DHT22(D17)
        file_name = self.get_csv_file_name(self.today())

        t = dt.datetime.now(dt.timezone(dt.timedelta(hours=+9), "Asia/Tokyo")).time()
        data = "\n{},{},{}".format(t.hour*60+t.minute, d.humidity, d.temperature)
        if not os.path.isfile(file_name):
            data = ",humidity,temperature" + data

        with open(file_name, "a") as f:
            f.write(data)

    def rename_xticklabes(self, old_label):
        new_label = [""] * len(old_label)
        for i,time in enumerate(old_label):
            if time < 1440:
                day = "{}-{}".format(self.yesterday.month, self.yesterday.day)
            else:
                day = "{}-{}".format(self.today.month, self.today.day)
                time -= 1440
            new_label[i] = "{}\n{}:00".format(day, int(time/60)) if time%60 == 0 else "{}\n{}:{}".format(day, int(time/60),int(time%60))
        return(new_label)

    def make_graph(self):
        df = pd.concat([pd.read_csv(self.get_csv_file_name(self.yesterday), index_col=0),
                        pd.read_csv(self.get_csv_file_name(self.today), index_col=0).rename(index=lambda i: i+1440)])
        fig, axs = plt.subplots(2,1, figsize=(7,6))
        fig.suptitle("Temperature and Humidity on the {}".format(self.today))
        last_time = df.index.values[-1]
        for ax, title in zip(axs, ("Temperature", "Humidity")):
            ax.plot(df[title.lower()], label=title)
            ax.set_title(title)
            ax.set_ylabel(title)
            ax.set_xlabel("time")
            ax.set_xlim(last_time - 1440, last_time)
            ax.legend()
            ax.grid(True)
            ax.set_xticks(ax.get_xticks())
            ax.set_yticks(ax.get_yticks())
            ax.set_xticklabels(self.rename_xticklabes(ax.get_xticks()))

        axs[0].set_yticklabels(["{}C".format(int(t)) if t.is_integer() else "{}C".format(t) for t in axs[0].get_yticks()])
        axs[1].set_yticklabels(["{}%".format(int(t)) if t.is_integer() else "{}%".format(t) for t in axs[1].get_yticks()])
        fig.tight_layout()
        file_name = Path(__file__).parent.resolve() / "graph.png"
        plt.savefig(file_name)
        plt.close()

def main():
    m = Measurement()
    m.measurement()
    m.make_graph()

if __name__ == "__main__":
    main()
