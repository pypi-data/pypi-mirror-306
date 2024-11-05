"""
This example generates an interactive plot with 3 noisy curves. This can be used
to test the builtin filtering functions.
"""

import numpy as np
import itrm

x = np.linspace(0, 1, 100_000)
y = np.zeros((3, len(x)))
for j in range(3):
    phi = 2*np.pi*j/3
    y[j] = 0.3*np.sin(2*np.pi*3*x + phi) \
            + 0.1*np.sin(2*np.pi*50*x + phi) \
            + 0.01*np.sin(2*np.pi*310*x + phi)
    y[j] += 0.05*np.random.randn(len(x))

itrm.iplot(x, y)
