# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 10:00:43 2022

@author: Rita
"""

# libreria di funzioni utili
import numpy as np
import math

def error(v1,v2,i):  #funzione per il calcolo delle incertezze statistiche 
    if i==0:
        return 0
    else:
        # math.sqrt((AV2[n] - AV[n]**2)/n)
        return math.sqrt((v2 - v1**2)/i)
    
# funzione per calcolare le medie a blocchi, deve restituire le somme 
# progressive e i quadrati di queste, che poi sono passati alla funzione
# per il calcolo delle incertezze statistiche 

def BlockMean(M1,M2,N):
    SumP1=np.zeros(N);
    SumP2=np.zeros(N);
    ErrorP=np.zeros(N);
    for i in range (N):
        for j in range (i+1):
            SumP1[i] += M1[j]
            SumP2[i] += M2[j]
            
        SumP1[i] /= i+1;
        SumP2[i] /= i+1;
        ErrorP[i] = error(SumP1[i], SumP2[i], i)
    return SumP1, ErrorP
    
def SimpleMean(Vector,N,L):
    M1=np.zeros(N)
    M2=np.zeros(N)
    for i in range (N):
        s=0
        for j in range(L):
            k=j+i*L
            s += Vector[k]
        M1[i]=s/L
        M2[i]=(M1[i])**2
    return M1, M2

def VarianceMean(Vector,Value,N,L):
    AVV1=np.zeros(N)
    AVV2=np.zeros(N)
    for i in range (N): # si implementa la media a blocchi
        s=0
        for j in range (L):
            k= j+ i*L
            s += (Vector[k]-Value)**2
        AVV1[i] = s/L
        AVV2[i] = (AVV1[i])**2
        
        
    return AVV1, AVV2


"""def SimpleMean(Vector,N, L):
    M1=np.zeros(N)
    M2=np.zeros(N)
    for i in range (N):
        s=0
        for j in range(L):
            k=j+i*L
            s += Vector[k]
            
        M1[i]=s/L
        M2[i]=(M1[i])**2
    return M1, M2


for i in range(N):
    sum1 = 0
    sum2 = 0 #PROVA per far vedere come si può sbagliare ad interpretare il calcolo di A_i^2
    for j in range(L):
        k = j+i*L
        sum1 += r[k]
        
    ave[i] = sum1/L     # r_i 
    
    av2[i] = (ave[i])**2 # (r_i)^2 

for i in range(N):
    for j in range(i+1):
        sum_prog[i] += ave[j] # SUM_{j=0,i} r_j
        su2_prog[i] += av2[j] # SUM_{j=0,i} (r_j)^2
    sum_prog[i]/=(i+1) # Cumulative average
    su2_prog[i]/=(i+1) # Cumulative square average
    err_prog[i] = error(sum_prog,su2_prog,i) # Statistical uncertainty"""
     
             