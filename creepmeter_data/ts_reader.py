

import h5py
import pandas as pd
import numpy as np
import datetime as dt
import os
import ts_obj  # local import


def read_slip_over_time(hdf5file, verbose=True):
    """
    Read the simplest and most general data from a creepmeter HDF5 file.
    Every file contains STA_combined, which has time and slip in mm.
    Not every file contains Temperature and Orthogonal fields,
    so in this function, we don't consider those.  This is meant to be the most general reader.

    :param hdf5file: name of HDF5 file, string
    :param verbose: default True
    :return: ts_obj from this creepmeter repo
    """
    with h5py.File(hdf5file, 'r') as f:
        keys = list(f.keys())
        # if verbose:
        #     print(keys)  # ex: ['KAR1_combined', 'Orthogonal', 'Temperature']
        for key in keys:
            if '_combined' in key:
                station_name = key.split('_')[0]
                data = f[key]  # Access the slip dataset
                data_keys = list(data.keys())
                if verbose:
                    print(key, ":", data_keys)
                slip = data[data_keys[0]][:]
                time = data[data_keys[1]][:]
                decoded_time = [byte_str.decode('utf-8') for byte_str in time]
                decoded_time = pd.to_datetime(decoded_time)
                obliquity = f.attrs['obliquity']
                lon, lat, network = f.attrs['longitude'], f.attrs['latitude'], f.attrs['network']
                slip = slip / np.cos(np.radians(obliquity))
    ts_trace = ts_obj.ts_obj(t=decoded_time, slip_mm=slip, station=station_name, lon=lon, lat=lat, network=network,
                             obliquity=obliquity)
    return ts_trace


def read_usgs_tenminute(filename, verbose=True):
    """
    Read a creepmeter time series from USGS, for example Nyland ranch, downloaded from here:
    https://earthquake.usgs.gov/monitoring/deformation/data/download.php

    NOTE: The conversion from float-day to datetime probably rounds incorrectly at the one-minute level.

    :param filename: string, filename
    :param verbose: default True
    :return: a Timeseries object
    """
    if verbose:
        print("Reading file %s " % filename)
    [year, decimal_date, value] = np.loadtxt(filename, unpack=True, usecols=(0, 1, 2))
    dtarray = []
    station = filename.split('/')[-1].split('.')[0]
    for i in range(len(year)):
        year_str = str(int(year[i]))
        doy = int(np.floor(decimal_date[i]))
        fractional_day = decimal_date[i] - doy   # something like 0.347000 (part of a day)
        number_of_minutes = fractional_day * (60*24)  # number of minutes past midnight
        hour = int(np.floor(number_of_minutes / 60))
        minutes = int(np.floor(number_of_minutes)) - hour*60  # minutes past the hour
        if hour < 10:
            hour_string = "0" + str(hour)
        else:
            hour_string = str(hour)
        if minutes < 10:
            minute_string = "0" + str(minutes)
        else:
            minute_string = str(minutes)
        if doy < 10:
            doy_str = "00"+str(doy)
        elif doy < 100:
            doy_str = "0"+str(doy)
        else:
            doy_str = str(doy)
        formatted_datetime = dt.datetime.strptime(str(year_str)+"-"+str(doy_str)+"-"+str(hour_string)
                                                  + "-" + str(minute_string), "%Y-%j-%H-%M")
        dtarray.append(formatted_datetime)
    metadata = pd.read_csv(os.path.split(filename)[0]+'/metadata.txt')
    row = metadata.loc[metadata["Abbreviation"] == station].iloc[0]
    ts_trace = ts_obj.ts_obj(t=dtarray, slip_mm=value, station=station, lon=row['Longitude'],
                             lat=row['Latitude'], network=row['Network'], obliquity="")
    return ts_trace


def read_multiple_ts(filelist, verbose=True):
    """
    Read the full dozens of time series from ALL hdf5 and USGS data records.
    Returns as a dictionary of traces, one for each station.

    :param filelist: - list of files that contain creepmeter time series information
    :param verbose: default True
    :returns: dictionary of ts_traces
    """
    dict_of_traces = {}
    for item in filelist:
        if '.h5' in item:
            ts_trace = read_slip_over_time(item, verbose=verbose)
        elif '.10min' in item:
            ts_trace = read_usgs_tenminute(item, verbose=verbose)
        else:
            continue
        dict_of_traces[ts_trace.station] = ts_trace
    return dict_of_traces
