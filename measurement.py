import adafruit_dht, board


class Measurement():
    def __init__(self, pin:board.pin):
        self.d = adafruit_dht.DHT22(pin)

    def get_humidity(self):
        return(self.d.humidity)

    def get_temperature(self):
        return(self.d.temperature)