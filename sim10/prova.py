# -*- coding: utf-8 -*-
"""
Created on Sun May 28 15:42:28 2023

@author: Rita
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import mpi4py 
from mpi4py import MPI


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
tstart = MPI.Wtime()

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
n = 100 
imesg = np.zeros(n)
imesg2 = np.zeros(n)
for i in range(n):
    imesg[i] = rank
    imesg2[i] = rank+1
    
if rank == 0:
    print(imesg)
    print(imesg2)
elif rank == 1:
    print(imesg)
    print(imesg2)

    
if rank == 0:
    comm.Send(imesg, dest=1)
    comm.Recv(imesg2, source=1)
    print('Io sono: ', rank,' Il mio messaggio: ',
          imesg2[0])
elif rank == 1:
    comm.Recv(imesg, source=0)
    comm.Send(imesg2, dest=0)
    print('Io sono: ', rank,' Il mio messaggio: ',
          imesg[0])








tend= MPI.Wtime()
print(tend-tstart)
MPI.Finalize()

