#!/usr/bin/env python3

import sys, re
import numpy as np
import matplotlib.pyplot as plt

dataFile = sys.argv[1]

xLabel = 'seconds'
yLabel = 'gram'

x = np.array([])
y = np.array([])

with open(dataFile) as f:
    for s_line in f:
        data = s_line.split()
        x = np.append(x, float(data[0]))
        y = np.append(y, float(data[1]))

plt.scatter(x, y, color="k", s=5)
plt.xlabel(xLabel)
plt.ylabel(yLabel)
plt.show()
