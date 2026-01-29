
import numpy as np
import pandas as pd


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
        if starttime is None and endtime is None:
            return self

        t = pd.to_datetime(self.t)
        start = pd.to_datetime(starttime) if starttime is not None else t.min()
        end = pd.to_datetime(endtime) if endtime is not None else t.max()

        time_mask = (t >= start) & (t <= end)
        t_clip = t[time_mask]
        slip_clip = np.asarray(self.slip_mm)[time_mask]

        orth_clip = None
        if self.orthogonal is not None:
            orth_clip = np.asarray(self.orthogonal)[time_mask]

        temp_t_clip = None
        temp_clip = None
        if self.temperature_t is not None and self.temperature is not None:
            temp_t = pd.to_datetime(self.temperature_t)
            temp_mask = (temp_t >= start) & (temp_t <= end)
            temp_t_clip = temp_t[temp_mask]
            temp_clip = np.asarray(self.temperature)[temp_mask]

        return ts_obj(
            t=t_clip,
            slip_mm=slip_clip,
            station=self.station,
            lon=self.lon,
            lat=self.lat,
            network=self.network,
            obliquity=self.obliquity,
            temp_t=temp_t_clip,
            temperature=temp_clip,
            orthogonal=orth_clip,
        )
