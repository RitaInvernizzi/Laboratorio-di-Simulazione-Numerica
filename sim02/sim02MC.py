# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 14:33:58 2022

@author: Rita
"""
import numpy as np
import math
from numpy import asarray
from numpy import savetxt
import MyFunctions as MF

# integrazione con sampling da distribuzione uniforme 

def integrand(x): #definisco la funzione integranda
    return np.pi*0.5*math.cos(np.pi*0.5*x)

def inv(r): # mi dà la funzione inversa
    x=1-math.sqrt(1-r);
    return x

def approx(x):
    return -2*x + 2

M=100000; # numero di campionamenti
N= 100; # blocchi
B= int(M/N); #campionamenti per blocco


Sample=np.random.rand(M); #vettore che contien i punti estratti 
FunValue=np.zeros(M);

for i in range (M):
    FunValue[i]=integrand(Sample[i]);
    
AV1=np.zeros(N);
AV2= np.zeros(N);


for i in range (N): # si implementa la media a blocchi
    s=0;
    for j in range (B):
        k= j+ i*B;
        s += FunValue[k];
    AV1[i] = s/B;
    AV2[i] = (AV1[i])**2;
  
# calcolo somme progressive e incertezze statistiche
SumProgr1, ErrSumP1 = MF.BlockMean(AV1,AV2,N);
IntU = asarray([SumProgr1])
ErrorU= asarray([ErrSumP1])
savetxt('IntU.txt', IntU, delimiter=',')
savetxt('ErrorU.txt', ErrorU, delimiter=',')
 # integrazione con il metodo dell'importance sampling 
 
Points=np.random.rand(M); # punti per fare inversione cumulativa 
AVI1=np.zeros(N);
AVI2= np.zeros(N);
Numerator= np.zeros(M);
Denom= np.zeros(M);

for i in range (M):
    Numerator[i]= integrand( inv(Points[i]));
    Denom[i]= approx( inv(Points[i]));
 
for i in range (N): # si implementa la media a blocchi
    s=0;
    for j in range (B):
        k= j+ i*B;
        s += Numerator[k]/Denom[k];
    AVI1[i] = s/B;
    AVI2[i] = (AVI1[i])**2;   


SumProgrI1, ErrSumPI1 = MF.BlockMean(AVI1,AVI2,N);
IntIS = asarray([SumProgrI1])
ErrorIS= asarray([ErrSumPI1])
savetxt('IntIS.txt', IntIS, delimiter=',')
savetxt('ErrorIS.txt', ErrorIS, delimiter=',')


# calcolo le varianze con le incetezze statistiche
# caso 1: distribuzione uniforme

AVV1=np.zeros(N);
AVV2= np.zeros(N);


for i in range (N): # si implementa la media a blocchi
    s=0;
    for j in range (B):
        k= j+ i*B;
        s += (FunValue[k]-1)**2;
    AVV1[i] = s/B;
    AVV2[i] = (AVV1[i])**2;

# calcolo somme progressive e incertezze statistiche
SumProgrV1, ErrSumPV1 = MF.BlockMean(AVV1,AVV2,N);

VarU = asarray([SumProgrV1])
ErrorVarU= asarray([ErrSumPV1])
savetxt('VarU.txt', VarU, delimiter=',')
savetxt('ErrorVarU.txt', ErrorVarU, delimiter=',')


#calcolo le varianze e le incertezze statistiche
#caso 2: importance sampling

AVVI1=np.zeros(N);
AVVI2= np.zeros(N);


for i in range (N): # si implementa la media a blocchi
    s=0;
    for j in range (B):
        k= j+ i*B;
        s += (-1+ Numerator[k]/Denom[k])**2;
    AVVI1[i] = s/B;
    AVVI2[i] = (AVVI1[i])**2;
  
# calcolo somme progressive e incertezze statistiche
SumProgrVI1, ErrSumPVI1 = MF.BlockMean(AVVI1,AVVI2,N);

VarIS = asarray([SumProgrVI1])
ErrorVarIS= asarray([ErrSumPVI1])
savetxt('VarIS.txt', VarIS, delimiter=',')
savetxt('ErrorVarIS.txt', ErrorVarIS, delimiter=',') 
