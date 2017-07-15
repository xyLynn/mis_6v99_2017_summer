# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sys
import numpy as np
a = np.arange(15).reshape(3,5)

sys.stdout = open('demo_numpy0.txt', 'w')
print(a)
print(a.shape)
print(a.size)
print(a.itemsize)
print(a.ndim)
print(a.dtype)

