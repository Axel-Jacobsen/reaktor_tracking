#! /usr/bin/env python3

import json
import itertools
import numpy as np
from datetime import datetime


def runoff_height(height_arr:np.array):
    """ given height array, returns an array that gives the height where
        each element of the height_arr will drain
        e.g. [2, 0, 1]
          => [2, 1, 1]
             [7, 7, 6, 5, 4, 4, 9, 8, 8, 7, 7, 7]
          => [7, 7, 7, 7, 7, 7, 9, 8, 8, 7, 7, 7]
             [8, 8, 5, 2]
          => [8, 8, 5, 2]
    """
    runoff_array = np.zeros(height_arr.shape)
    prev_height = np.min(height_arr)
    for i, h in enumerate(height_arr):
        if prev_height < h:
            prev_height = h
            runoff_array[i] = h
        else:
            runoff_array[i] = prev_height

    prev_height = np.min(height_arr)
    for i, h in enumerate(height_arr[::-1]):
        rev_i = len(height_arr) - i - 1
        if prev_height < h:
            prev_height = h
            runoff_array[rev_i] = min(h, runoff_array[rev_i])
        else:
            runoff_array[rev_i] = min(prev_height, runoff_array[rev_i])

    return runoff_array


def split_arr_on_val(arr:list, val):
    groups = []
    curr_group = []
    for v in arr:
        if v != 0:
            curr_group.append(v)
        else:
            if len(curr_group) != 0:
                groups.append(curr_group)
                curr_group = []
    return groups


def get_volume(arr:list):
    nparr = np.asarray(arr)
    runoff_arr = runoff_height(nparr)
    columns = runoff_arr - nparr
    holes = split_arr_on_val(columns, 0)
    if len(holes) == 0:
        return 0
    return max([sum(v) for v in holes])


def test_pooling():
    vol_1 = {
            'val': 1,
            'arrs': [
                [1, 0, 1],
                [1, 0, 2],
                [2, 0, 1],
                [-1, -2, -1],
                ]
            }
    vol_4 = {
            'val': 4,
            'arrs': [
                [3, -1, 3, 1, 3, 3, 1],
                [3, 2, 3, 0, 2, 3, 1],
                [0, 1, 2, -2, 2, 1, 0],
                ]
            }
    test_pkts = [vol_1, vol_4]
    for pkt in test_pkts:
        for test_arr in pkt['arrs']:
            assert pkt['val'] == get_volume(test_arr)


if __name__ == '__main__':

    test_pooling()

    with open('flood.txt', 'r') as f:
        # regionID: str
        # readings: array of altitudes
        # date: str
        json_dat = json.loads(f.read())['regions']

        condensed = {}
        for region in json_dat:
            condensed[region['regionID']] = sorted(
                    [
                        {
                            'readingID': reading['readingID'],
                            'vol': get_volume(reading['reading']),
                            'date': datetime.strptime(reading['date'], '%d-%b-%Y')
                        }
                    for reading in region['readings']
                    ],
                key=lambda v: v['date']
            )

        for regionID in condensed.keys():
            prev_vol = condensed[regionID][0]['vol']
            prev_day = condensed[regionID][0]['date']
            for reading in condensed[regionID]:
                if abs(prev_vol - reading['vol']) > 1000 and (reading['date'] - prev_day).days == 1:
                    print(regionID, reading['readingID'], abs(prev_vol - reading['vol']), prev_day, reading['date'])
                prev_vol = reading['vol']
                prev_day = reading['date']



