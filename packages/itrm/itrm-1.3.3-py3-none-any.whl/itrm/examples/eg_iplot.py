"""
This example shows an interactive plot with 6 different sine waves, each out of
phase from the other.
"""

import numpy as np
import itrm

# Constants
K = 200000
J = 6

# x axis
x = np.linspace(0, 1, K)

# y axis data
Y = np.zeros((J, len(x)))
for j in range(J):
    Y[j] = np.cos(2*np.pi*2*x + (j/J)*np.pi)

# plot
labels = ["Fruit", "Plum", "Grape", "Apple", "Banana", "Orange", "Cherry"]
itrm.iplot(x, Y, label=labels, uni=True)
