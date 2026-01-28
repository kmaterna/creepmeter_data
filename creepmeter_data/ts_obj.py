

class ts_obj:
    def __init__(self, t, slip_mm, station, lon, lat, network, obliquity,
                 temp_t=None, temperature=None, orthogonal=None):
        self.t = t  # time in UTM
        self.slip_mm = slip_mm  # slip in mm
        self.station = station  # station name, str
        self.lon = lon  # lon in degrees
        self.lat = lat  # lat in degrees
        self.network = network  # network, str
        self.obliquity = obliquity  # obliquity in degrees
        self.temperature = temperature  # optional temperature time series
        self.temperature_t = temp_t   # optional time axis of temperature time series
        self.orthogonal = orthogonal  # optional orthogonal time series

    def clip_to_time(self, starttime, endtime):
        return
