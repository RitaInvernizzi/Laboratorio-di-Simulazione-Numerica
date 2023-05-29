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

#Random Walk su reticolo 3d e continuo con media a blocchi
# Caso 1: RW su Reticolo  
# Caso2:Rw continuo

np.random.seed=0
N= 100 # numero di passi (blocchi)
M = 10000 # numero totale di RW
T= int(M/N) # numero di RW per blocco

dist_C = np.zeros(N) # distanza caso continuo
dist_C2 = np.zeros(N) # distanza^2 caso continuo, serve per la media a blocchi

dist_D = np.zeros(N) # distanza caso discreto
dist_D2= np.zeros(N) #  distanza^2 discreta, serve per la media a blocchi


for i in range(M): # realizzo il rw
    xd=0 #inizializzazione del punto di partenza per tutti e due i casi
    yd=0
    zd=0
    
    xc=0
    yc=0
    zc=0
    
    
    for j in range(N-1):
        # caso discreto
        index = np.random.random()
        a=0 #definisco lo step unitario
        if index >= 0.5: # o lo step è positivo o negativo
           a = 1
        else:
             a = -1
        RDirection = np.random.randint(1,4) #scelgo la direzione dello step, dx, sx, su o giù
        if RDirection == 1: # direzione x
           xd += a
           
        elif RDirection == 2: #direzione y
             yd += a
        else: #altrimenti z
             
             zd += a
        
        #caso continuo: uso le coordinate polari sferiche
        Phi= 2*(math.pi)*np.random.rand() # definisco i due angoli theta e phi
        Theta= (math.pi)*np.random.rand()
        xc += math.sin(Theta)*math.cos(Phi)  #genero le coordinate
        yc += math.sin(Theta)*math.sin(Phi) 
        zc += math.cos(Theta) 
        
        rd = xd*xd + yd*yd + zd*zd
        rc = xc*xc + yc*yc +zc*zc
        dist_C[j+1] += rc
        dist_C2[j+1] += rc*rc
        dist_D[j+1] += rd
        dist_D2[j+1] = rd*rd
        


RadC = np.zeros(N)
RadD =np.zeros(N)
EC =np.zeros(N)
ED =np.zeros(N)
Mdist_C = np.zeros(N)
Mdist_C2 = np.zeros(N)

Mdist_D = np.zeros(N)
Mdist_D2= np.zeros(N)


epsilon = 1*10**(-4) # corresione per evitare errori dovuti alla precisione con cui sono gestiti i float e non avere valori negativi sotto radice
for k in range(N): # calcolo medie a bocchi ed errore con propagazione la propagazione dell'errore
    dist_D[k] = dist_D[k]/M
    dist_C[k] = dist_C[k]/M
    
    dist_D2[k] = dist_D2[k]/M
    dist_C2[k] = dist_C2[k]/M
    
    Mdist_D[k] = dist_D[k]/M
    Mdist_C[k] = dist_C[k]/M
    
    Mdist_D2[k] = dist_D2[k]/M
    Mdist_C2[k] = dist_C2[k]/M
    
    RadC[k] = np.sqrt(dist_C[k])
    RadD[k] = np.sqrt(dist_D[k])
    
    if k==0:
        EC[k]=0
        ED[k]=0
    else:
        ED[k] = 1./2 * pow(dist_D[k], -1./2) * np.sqrt((Mdist_D2[k] - Mdist_D[k] * Mdist_D[k] + epsilon ) / k);
        EC[k] = 1./2 * pow(dist_C[k], -1./2) *np.sqrt((Mdist_C2[k] - Mdist_C[k] * Mdist_C[k] + epsilon) / k);
        print(ED[k])
        print(EC[k])
        
# salvo i dati
        
        
np.save('RadC.npy', RadC)
np.save('RadD.npy', RadD)
np.save('EC.npy', EC)
np.save('ED.npy', ED)
    
    
    
    
    
    






    

        
    







