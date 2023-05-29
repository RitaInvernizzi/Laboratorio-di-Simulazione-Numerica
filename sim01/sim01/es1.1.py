# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 15:45:22 2022

@author: Rita
"""

import numpy as np
import math
from numpy import asarray
from numpy import savetxt
import MyFunctions as MF
import matplotlib
import matplotlib.pyplot as plt


# test di un generatore di numeri random tra 0 e 1, verificare valore medio,
# deviazione standard etc
    
T= 100000; # numero di lanci
N= 100; # numero di blocchi
L=int(T/N); # lanci per blocco
np.random.seed(0); #fisso seed

r=np.random.rand(T);
x=np.arange(N);

#definisco i vettori per le medie  & calcolo gli errori
mean1=np.zeros(N);
mean2=np.zeros(N);
errorSum=np.zeros(N);
CumSum=np.zeros(N);
CumSum2=np.zeros(N);
ErrorSP= np.zeros(N);

for i in range (N):   
    s=0;  
    for j in range (L):
        k = j+i*L
        s += r[k]     
    mean1[i]=s/L
    mean2[i]=(mean1[i])**2
 
 # calcolo medie cumulate e medie cumulate quadratiche
 

CumSum, ErrorSP =MF.BlockMean(mean1,mean2,N);
#salvo i risultati
x*=L;
myData = asarray([CumSum]);
myError= asarray([ErrorSP]);
axes= asarray([x]);
savetxt('myData.txt', myData, delimiter=',');
savetxt('myError.txt', myError, delimiter=',');
savetxt('axes.txt', axes, delimiter=',');

# Calcolo delle incertezze statistiche
M1= np.zeros(N);
M2= np.zeros(N);
SP= np.zeros(N);
SP2= np.zeros(N);
ESP= np.zeros(N)

for i in range (N):
    s=0;
    for j in range (L):
        k = j+i*L;
        s += (r[k] - 0.5)**2;
    M1[i] = s/L;
    M2[i] = (M1[i])**2;
 
SP, ESP = MF.BlockMean(M1,M2,N);
   
myData1 = asarray([SP]);
myError1= asarray([ESP]);
savetxt('myData1.txt', myData, delimiter=',');
savetxt('myError1.txt', myError, delimiter=',');

## Analisi del chi quadro
Steps=100;
Interval= np.linspace(0,1,num=Steps+1);
Attempts=10000;
Numbers=np.random.rand(Steps,Attempts);      
Hist=np.zeros((Steps,Steps-1));

for i in range (Steps): #righe matrice = righe Hist
    for j in range (Attempts):
        for k in range (Steps-1):
            element= Numbers[i,j];
            start=Interval[k];
            end=Interval[k+1];
            if start<element<end:
                Hist[(i,k)] += 1;

#calcolo il chi quadro
Chi= np.zeros(Steps);
for i in range (Steps):
    for j in range (Steps-1):
        Chi[i] += (Hist[(i,j)]-Steps)**2 / Steps


np.save('Chi.npy',Chi)
    








