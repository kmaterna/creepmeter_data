

import h5py
import pandas as pd
import numpy as np


def read_slip_over_time(hdf5file):
    """
    Read the simplest and most general data from a creepmeter HDF5 file.
    Every file contains STA_combined, which has time and slip in mm.
    Not every file contains Temperature and Orthogonal fields,
    so in this function, we don't consider those.  This is meant to be the most general reader.

    :param hdf5file: name of HDF5 file
    :return: time in UTM, slip in mm, lon, lat, and obliquity in degrees, station_name, network
    """
    with h5py.File(hdf5file, 'r') as f:
        keys = list(f.keys())
        # print(keys)  # ex: ['KAR1_combined', 'Orthogonal', 'Temperature']
        for key in keys:
            if '_combined' in key:
                station_name = key.split('_')[0]
                data = f[key]  # Access the slip dataset
                data_keys = list(data.keys())
                print(key, ":", data_keys)
                slip = data[data_keys[0]][:]
                time = data[data_keys[1]][:]
                decoded_time = [byte_str.decode('utf-8') for byte_str in time]
                decoded_time = pd.to_datetime(decoded_time)
                obliquity = f.attrs['obliquity']
                lon, lat, network = f.attrs['longitude'], f.attrs['latitude'], f.attrs['network']
                slip = slip / np.cos(np.radians(obliquity))

    return decoded_time, slip, lon, lat, obliquity, station_name, network
