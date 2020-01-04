#! /usr/bin/env python3

from collections import deque
import matplotlib.pyplot as plt


def longest_unique_char_str(line):
    cbuff = deque(maxlen=15)
    i = msg_start = 0
    ls = []

    while i < len(line):
        if line[i] not in cbuff:
            msg_start += 1
        else:
            msg_start = 1

        ls.append(msg_start)

        if msg_start == 16:
            return ''.join(list(cbuff)) + line[i]

        cbuff.append(line[i])
        i += 1

    plt.plot(range(len(ls)), ls)
    plt.show()


with open('b64msg.txt', 'r') as f:
    line = f.readline()
    print(longest_unique_char_str(line))
    # Curtisisland

