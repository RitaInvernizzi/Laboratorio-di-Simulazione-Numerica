# -*- coding: utf-8 -*-
"""
Created on Sun May 28 21:01:57 2023

@author: Rita
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import MyFunctions as MF
import mpi4py 
from mpi4py import MPI


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
tstart = MPI.Wtime()


def PsiOne(x,y,z): # gs, è già il mod^2  di psi
    r= math.sqrt(x**2 + y**2 + z**2)
    return math.exp(-2*r)/math.pi

def PsiTwo(x,y,z): # primo stato eccitato
    r= math.sqrt(x**2 + y**2 + z**2)
    return (r**2)*math.exp(-r)/(math.pi*32)*np.power(np.cos(np.arctan2(y,x)),2)

def Segno(): #funzione che definisce la direzione del passo
    ind= np.random.rand()
    a=0
    if ind>=0.5:
       a=+1
    else:
        a=-1
    return a

def Metropolis(x0, y0,z0, step, choice): 
    x= Segno()*step*np.random.rand()+x0 #genero le nuove coordinate estraendo da una prob uniforme
    y= Segno()*step*np.random.rand()+y0
    z= Segno()*step*np.random.rand()+y0
    if choice == 0:
       A= PsiOne(x,y,z)/PsiOne(x0, y0,z0)
    else:
         A= PsiTwo(x,y,z)/PsiTwo(x0, y0,z0)
         
    alpha= min(1,A)
    r= np.random.rand();
    if r<=alpha:
       x1=x
       y1=y
       z1=z
    else:
        x1=x0
        y1=y0
        z1=z0
    return x1, y1, z1, alpha


#definisco l'origine 
np.random.seed=0
x0=0 # questi li scelgo come i massimo delle due distribuzioni di probabilità
y0=0
a=0.0529
z0=math.sqrt(1/2)/a #scrivo le lunghezze in unità di raggio di bohr
step=1.1 #lo scelgo in modo da avere una probabilità di accettazione di 0.5
choice=0 # studio lo stato fondamentale

M=1000000
N= 100
Accept=np.zeros(M)
Radius= np.zeros(M)
a=x0
b=y0
c=z0
for i in range(M):
    x1,y1,z1,Accept[i]= Metropolis(a,b,c, step, choice)
    Radius[i]= math.sqrt(x1**2 + y1**2 +z1**2)
    a=x1
    b=y1
    c=z1
    

L=int(M/N)
M1,M2 =MF.SimpleMean(Radius,N,L)
# raggio sf uniform
MeanRad, ErrorRad= MF.BlockMean(M1,M2,N)
np.save('radGSuniformSN.npy', MeanRad, allow_pickle=True, fix_imports=True)
np.save('ErrorGSuniformSN.npy', ErrorRad, allow_pickle=True, fix_imports=True)

tend= MPI.Wtime()
print(tend-tstart)
MPI.Finalize()
