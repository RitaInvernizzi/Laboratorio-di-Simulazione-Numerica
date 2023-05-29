# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 22:56:47 2022

@author: Rita
"""
### CONDIZIONE DI SUCCESS0 DI UN LANCIO DELL'AGO SULLA GRIGLIA 
## Quando l'ago cade sulla griglia, questo forma con le linee verticali un angolo
### THETA. la condizione di intersezione tra le righe verticali e l'ago è definita
### da: x < l *0.5 *sin(theta), dove x e theta sono due variabili casuali indipendenti, 
###estratte da distribuzioni uniformi tra [0,1]  e  tra  [0, pi].
import numpy as np

angles = np.linspace(-np.pi, np.pi, 10000)
n = len(angles)
circ = 0
for i in range(n-1):
    step = np.power((np.cos(angles[i+1]) - np.cos(angles[i])),2) + np.power((np.sin(angles[i+1]) - np.sin(angles[i])),2) 
    circ += np.sqrt(step)

pi_ext = 0.5*circ
print('This is the extimation for pi: ', pi_ext)


np.random.seed=0
d=2.0 #distanza tra le linee verticali

l=1.0 # lunghezza dell'ago
K=2*l/d
M=30000 #numero di tentativi;
N =100 # numero di tentativi per blocco
L= int(M/N)
smPi = 0
smPi2 = 0
Pi_e = np.zeros(N)
Error_Pi = np.zeros(N)

for i in range(N):
    Pi = 0
    N_hit = 0
    
    for j in range(L):
        x = np.random.rand()
        theta = pi_ext*np.random.rand()
        if x<= 0.5*np.sin(theta):
            N_hit += 1
        
        if N_hit != 0:
            
            Pi += (2 * l * j) / (N_hit * d)
    
    smPi += Pi/L
    smPi2 += (Pi/L)*(Pi/L)
    sumCumPi = smPi/(i+1)
    sumCumPi2 = smPi2 /(i+1)
    Pi_e[i] = sumCumPi
    if(i==0):
        Error_Pi[i] = 0
    else:
        Error_Pi[i] = np.sqrt((sumCumPi2-sumCumPi*sumCumPi)/i)
        
        

    
    
np.save('Pi.npy', Pi_e)
np.save('Error_Pi.npy', Error_Pi)








