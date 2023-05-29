# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 17:49:29 2023

@author: Rita
"""

import numpy as np

import matplotlib.pyplot as plt

np.random.seed=1

# le funzioni Exponential Lorentz_Cauchy generano numeri casuali distribuiti 
#secondo le distribuzioni  esponenziali e di Cauchy Lorentz (Lambda = 1 e Gamma = 1)
# Il metodo utilizzato per generare i numeri casuali secondo le due distribuzioni
# è l'inverse transform sampling
def Exponential(Lambda):
    return -(1/Lambda)*np.log(1-np.random.rand())

def Lorentz_Cauchy():
    return np.tan(np.pi*(0.5-np.random.rand()))

def exponetial_vect(Lambda,Realization,N):
   
    throws=N
    Vector=np.zeros(Realization)
    for i in range (Realization):
        for j in range(throws):
            Vector[i] += Exponential(1)
        
        Vector[i] = Vector[i]/throws
            
    return Vector

Vector= exponetial_vect(1,np.power(10,4), 100)
H, Edges= np.histogram(Vector,bins=100)
Centres=np.zeros(100)
for p in range(len(Edges)-1):
    Centres[p]=(Edges[p+1]+Edges[p])*0.5
fig1, ax1=plt.subplots(figsize=(12,10))    
ax1.bar(Centres,H)


def Lorentz_Cauchy_vector(Realization,N):
    
    throws=N
    Vector=np.zeros(Realization)
    for i in range (Realization):
        for j in range(throws):
            Vector[i] += Lorentz_Cauchy()
        
        Vector[i] = Vector[i]/throws
        
    return Vector


Vector= Lorentz_Cauchy_vector(np.power(10,4), 100)
H, Edges= np.histogram(Vector,bins=100)
plt.title('Expoonential')
Centres=np.zeros(100)
for p in range(len(Edges)-1):
    Centres[p]=(Edges[p+1]+Edges[p])*0.5
    


fig2, ax2=plt.subplots(figsize=(12,10))   
plt.title('Cauchy') 
ax2.plot(Centres,H)

def Dice(Realization, throws):
    
    
    Vector=np.zeros(Realization)
    for i in range (Realization):
        for j in range(throws):
            Vector[i] += np.random.randint(1,7)
            
        Vector[i] = Vector[i]/throws
            
    return Vector

throws=100
Vector_Dice= Dice(np.power(10,4),throws)
H, Edges= np.histogram(Vector_Dice,bins=100)
Centres=np.zeros(100)
for p in range(len(Edges)-1):
    Centres[p]=(Edges[p+1]+Edges[p])*0.5
    


fig3, ax3=plt.subplots(figsize=(12,10))   
plt.title('Dice') 
ax3.bar(Centres,H)

# valori di N per cui si valuta S_n

attempts = np.array([2,10,30,50,75,100])

Iter = len(attempts)

#esponenziale
exp_vect= np.zeros((Iter, np.power(10,4)))

Lambda=1
Realization = np.power(10,4)
for i in range(Iter):
    exp_vect[i,:] = exponetial_vect(Lambda,Realization, attempts[i])
    
cauchy_vect = np.zeros((Iter, np.power(10,4)))
for i in range(Iter):
    cauchy_vect[i,:] = Lorentz_Cauchy_vector(Realization,attempts[i])


Dice_vect= np.zeros((Iter, np.power(10,4)))
for i in range(Iter):
    Dice_vect[i,:] = Dice(Realization,attempts[i])


np.save('exp_vect.npy', exp_vect, allow_pickle=True, fix_imports=True)
np.save('cauchy_vect.npy',cauchy_vect, allow_pickle=True, fix_imports=True)
np.save('Dice_vect.npy', Dice_vect, allow_pickle=True, fix_imports=True)



