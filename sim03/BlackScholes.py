# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 09:34:07 2022

@author: Rita
"""

import numpy as np
import math
from numpy import asarray
from numpy import savetxt
import MyFunctions as MF

# definisco le funzioni per calcolare il moto geometrico browniano

M = 10000
N = 100
T = 1 #delivery time
r = 0.1 #rate
sigma = 0.25 #volatility
SO = 100
t=0
K=100
# calcolo di S(T) via montecarlo
# Metodo campionamento diretto

#ST=np.zeros(M)
CallC=np.zeros(M)
PutC=np.zeros(M)

# sampling continuo
for i in range (M):
    z=np.random.normal(0,T)
    ST= SO * math.exp((r-0.5*sigma**2)*T + sigma* z* math.sqrt(T))
    CallC[i]=math.exp(-r*T)*max([0,ST-K])
    PutC[i]=math.exp(-r*T)*max([0,K-ST])
               
 # sampling discreto  
CallD=np.zeros(M)
PutD=np.zeros(M)
times=np.linspace(0,1,N+1)

for i in range (M):
    start=SO
    for j in range (N):
        z=np.random.normal(0,T)
        ST=start* math.exp((r-0.5*sigma**2)*0.01 + sigma* z* math.sqrt(0.01))
        start=ST
    CallD[i]=math.exp(-r*T)*max([0,ST-K])
    PutD[i]=math.exp(-r*T)*max([0,K-ST])


#calcolo valori medi e incertezze con data blocking
L=int(M/N)
MCallD=np.zeros(N)
MPutD=np.zeros(N)
MCallC=np.zeros(N)
MPutC=np.zeros(N)
M2CallD=np.zeros(N)
M2PutD=np.zeros(N)
M2CallC=np.zeros(N)
M2PutC=np.zeros(N)

for i in range (N):
    p=0
    q=0
    r=0
    s=0
    for j in range(L):
        k= j + i*L
        p += CallC[k]
        q += PutC[k]
        r += CallD[k]
        s += PutD[k]
    MCallD[i]= r/L
    MPutD[i]=  s/L
    MCallC[i]= p/L
    MPutC[i]= q/L
    M2CallD[i]= (MCallD[i])**2
    M2PutD[i]=  (MPutD[i])**2
    M2CallC[i]= (MCallC[i])**2
    M2PutC[i]=  (MPutC[i])**2

SCallC, SECallC= MF.BlockMean(MCallC,M2CallC,N)
SCallD, SECallD= MF.BlockMean(MCallD,M2CallD,N)
SPutC, SEPutC= MF.BlockMean(MPutC,M2PutC,N)
SPutD, SEPutD= MF.BlockMean(MPutD,M2PutD,N)

Names1=['SCallC','SECallC','SPutC','SEPutC','SCallD','SECallD','SPutD','SEPutD']
Names=['''SCallC.txt''','''SECallC.txt''','''SPutC.txt''','''SEPutC.txt''','''SCallD.txt''','''SECallD.txt''','''SPutD.txt''','''SEPutD.txt''']
Datas= [[SCallC],[SECallC],[SPutC],[SEPutC],[SCallD],[SECallD],[SPutD],[SEPutD]]

for i in range (8):
    Names1[i]=asarray(Datas[i])
    savetxt(Names[i], Names1[i], delimiter=',');
      