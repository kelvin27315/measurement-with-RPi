#!/usr/bin/env python

"""
温度を表示する
"""

import Adafruit_DHT as dht

humidity, temperature = dht.read_retry(dht.AM2302, 2)

print("湿度:\t{:.1f}%".format(humidity))
print("温度:\t{:.1f}℃".format(temperature))