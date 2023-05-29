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
        return math.sqrt((v2[i] - v1[i]**2)/i)
    
# funzione per calcolare le medie a blocchi, deve restituire le somme 
# progressive e i quadrati di queste, che poi sono passati alla funzione
# per il calcolo delle incertezze statistiche 


def BlockMean(M1,M2,N):
    SumP1=np.zeros(N);
    SumP2=np.zeros(N);
    ErrorP=np.zeros(N);
    
    for i in range (N):
        for j in range (i+1):
            SumP1[i] += M1[j];
            SumP2[i] += M2[j];
        SumP1[i] /= i+1;
        SumP2[i] /= i+1;
        if i==0:
            ErrorP[i]=0;
        else:
            ErrorP[i]=math.sqrt((SumP2[i]-SumP1[i]**2)/i);
            
            
    return SumP1, ErrorP
    
    