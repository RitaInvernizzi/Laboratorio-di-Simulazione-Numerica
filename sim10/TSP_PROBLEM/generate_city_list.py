# -*- coding: utf-8 -*-
"""
Created on Sat May 20 11:34:00 2023

@author: Rita
"""

import numpy as np

data = np.loadtxt( 'American_capitals.dat', skiprows= 0, usecols=[2,3])

text_file = open("American_capitals.dat", "r")
#read whole file to a string
names = text_file.read()
#close file
text_file.close()
print(names)


