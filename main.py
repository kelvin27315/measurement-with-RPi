#!/usr/bin/env python

from weather_observation_result import WeatherObservationResult
from pathlib import Path
from measurement_data import MeasurementData
from board import D17
import datetime as dt

def main():
    pin = D17
    dir_path = Path(__file__).parent.resolve()
    md = MeasurementData()
    md.update_to_current_data(dir_path/"data", pin)
    df = md.read_newest_csv(dir_path/"data")
    wor = WeatherObservationResult()
    wor.make_graph(df, dir_path/"graph.png")

if __name__ == "__main__":
    main()
