import matplotlib.pyplot as plt
import datetime as dt

class WeatherObservationResult():
    def __init__(self):
        self.today = dt.date.today()
        self.yesterday = self.today - dt.timedelta(days=1)

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

    def make_graph(self, df ,file_path):
        fig, axs = plt.subplots(2,1, figsize=(7,6))
        fig.suptitle("Temperature and Humidity on the {}".format(self.today))
        last_time = df.index.values[-1]
        return_unit = {"Temperature":"C", "Humidity":"%"}
        for ax, title in zip(axs, ("Temperature", "Humidity")):
            ax.plot(df[title.lower()], label=title)
            yticks = ax.get_yticks()
            ax.set_title(title)
            ax.set_xlabel("time")
            ax.set_xlim(last_time - 1440, last_time)
            ax.set_xticks(ax.get_xticks())
            ax.set_xticklabels(self.rename_xticklabes(ax.get_xticks()))
            ax.set_ylabel(title)
            ax.set_ylim(yticks[0],yticks[-1])
            ax.set_yticks(ax.get_yticks())
            ax.set_yticklabels([str(round(t,1))+return_unit[title] for t in ax.get_yticks()])
            ax.vlines(1440, ax.get_yticks()[0], ax.get_yticks()[-1], "red", "dashed")
            ax.legend()
            ax.grid(True)
        fig.tight_layout()
        plt.savefig(file_path)
        plt.close()
