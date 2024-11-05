"""
This example shows how interactive plots handle the case where only the `x`
input, which is then treated as the y axis, is provided.
"""

import numpy as np
import itrm

# Constants
K = 100000

x = np.linspace(0, 1, K)
y = np.cos(2*np.pi*2*x)

itrm.iplot(y)
