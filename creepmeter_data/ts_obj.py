
import numpy as np
import pandas as pd
import datetime as dt


class ts_obj:
    def __init__(self, t, slip_mm, station, lon, lat, network, obliquity,
                 temp_t=None, temperature=None, orthogonal=None):
        self.t = t  # time in UTM, pandas dt?
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
        """ What type is starttime, endtime?  I think it's basically a string."""
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

    def normalize_ts(self):
        return ts_obj(
            t=self.t,
            slip_mm=self.slip_mm / self.slip_mm.max,
            station=self.station,
            lon=self.lon,
            lat=self.lat,
            network=self.network,
            obliquity=self.obliquity,
            temp_t=self.temperature_t,
            temperature=self.temperature,
            orthogonal=self.orthogonal,
        )

    def get_velocity(self):
        delta = self.t[1] - self.t[0]  # assumes a single sampling rate for everything
        seconds = delta.total_seconds()
        slip_m = self.slip_mm / 1000  # slip in meters
        # velocity = np.diff(slip_m) / seconds  # in meters per second, single difference
        velocity = (slip_m[2:] - slip_m[0:-2]) / (2 * seconds)  # m/s, use two points for smoothed velocity
        time = self.t[1:-1]  # should make this the middle of the window actually
        return time, velocity

    def display_sampling_rate_info(self, verbose=True):
        """
        Return info about the sampling rate in the time series.
        Returns the sampling intervals themselves, the unique sampling intervals, and the amounts of each.
        """
        seconds, counts = [], []
        for i in range(len(self.t)-1):
            temp = self.t[i+1] - self.t[i]
            seconds.append(temp.total_seconds())
        seconds = np.array(seconds)
        unique_intervals = set(seconds)
        for time_interval in unique_intervals:
            counts.append(len(seconds[seconds == time_interval]))
        total_time = (self.t[-1] - self.t[0]).total_seconds()
        average_sampling = total_time / (len(self.t)-1)
        if verbose:
            print("Time series has "+str(len(self.t))+" points from " +
                  dt.datetime.strftime(self.t[0], "%Y-%m-%d %H:%M:%S")
                  + " to "+dt.datetime.strftime(self.t[-1], "%Y-%m-%d %H:%M:%S") + " in " + str(len(unique_intervals))
                  + " unique sampling intervals")
            print("Average spacing = " + str(average_sampling) + " seconds")
            for i, (x, y) in enumerate(zip(unique_intervals, counts)):
                print(i, ':', x, ':', y)
        return seconds, set(seconds), counts
