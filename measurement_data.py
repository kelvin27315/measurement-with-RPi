from measurement import Measurement
from pathlib import Path
import datetime as dt
import pandas as pd
import board, os


class MeasurementData():
    def __create_file(self, file_path: Path) -> None:
        with open(file_path, "w") as f:
            f.write(",humidity,temperature")

    def update_to_current_data(self, dir_path: Path, pin) -> None:
        m = Measurement(pin)
        t = dt.datetime.now(dt.timezone(dt.timedelta(hours=+9), "Asia/Tokyo")).time()
        data = "\n{},{},{}".format(t.hour*60 + t.minute,m.get_humidity(),m.get_temperature())
        
        file_path = dir_path / "{}.csv".format(dt.date.today())
        if not os.path.isfile(file_path):
            self.__create_file(file_path)
        with open(file_path, "a") as f:
            f.write(data)

    def read_csv(self, dir_path: Path , day: dt.date) -> pd.DataFrame:
        day_file_path = dir_path / "{}.csv".format(day)
        previousday_file_path = dir_path / "{}.csv".format(day - dt.timedelta(days=1))
        
        if os.path.isfile(previousday_file_path):
            df = pd.concat([pd.read_csv(previousday_file_path, index_col=0),
                            pd.read_csv(day_file_path, index_col=0).rename(index=lambda i: i+1440)])
        else:
            df = pd.read_csv(day_file_path, index_col=0).rename(index=lambda i: i+1440)
        return(df)

    def read_newest_csv(self, dir_path: Path) -> pd.DataFrame:
        return(self.read_csv(dir_path, dt.date.today()))