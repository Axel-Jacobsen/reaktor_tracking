#! /usr/bin/env python3

import json
import numpy as np
from functools import reduce


def byte_to_int(byte):
    tot = 0
    for i in range(8):
        tot += int(byte[7 - i]) * 2 ** i
    return tot


def get_average(dat: list):
    tot = sum([v['val'] for v in dat])
    return tot / len(dat)


def get_variance(dat: list):
    avg = get_average(dat)
    return np.sqrt(sum([(x['val'] - avg) ** 2  for x in dat]) / (len(dat) - 1))

def hex_to_ascii(v_id):
    id_str = ''
    for i in range(0, 14, 2):
        id_str = id_str + chr(int(v_id[i - 14] + v_id[i - 14 + 1], 16))

    return id_str

if __name__ == '__main__':
    with open('ppb.bin.log', 'r') as f:
        data = ''.join([chr(byte_to_int(b)) for b in f.read().split(' ')])
        json_data = json.loads(data)
        totals = []
        for day in json_data:
            for reading in day['readings']:
                totals.append({
                    'val': sum(reading['contaminants'].values()),
                    'id': reading['id']
                })

        variance = get_variance(totals)
        totals_avg = get_average(totals)
        samples_outside_variance = list(filter(lambda x: not ((totals_avg - variance) < x['val'] < (totals_avg + variance)), totals))
        assert len(samples_outside_variance) == 1
        sample = samples_outside_variance[0]

        print(f'variance: {variance}')
        print(f'avg: {totals_avg}')
        print(f'id: {sample["id"]}')
        print(f'location: {hex_to_ascii(sample["id"])}')


