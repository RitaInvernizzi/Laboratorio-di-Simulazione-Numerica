# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 21:55:12 2023

@author: Rita
"""

import numpy as np
import library as lb
import matplotlib.pyplot as plt



City_numb=34
Phi=2*np.pi*np.random.rand(34)
Phi[0]=np.pi*0.5
City_list=np.empty((34,3))
temporary=np.empty((34,3))
for i in range(City_numb):
    City_list[i,:]=np.array([i,np.cos(Phi[i]),np.sin(Phi[i])])
    temporary[i,:]=np.array([i,np.cos(Phi[i]),np.sin(Phi[i])])

Population_size=100
Population=np.empty((34,3,Population_size))


for i in range(Population_size): #generate population
    Population[0,:,i]=np.array([i*0,np.cos(Phi[0]),np.sin(Phi[0])])
    np.random.shuffle(City_list[1:34])
    Population[1:34,:,i]=City_list[1:34]
    #apply check
    DoItAgain=lb.check2(Population[:,:,i],temporary)
    while DoItAgain==True:
        np.random.shuffle(City_list[1:34])
        Population[1:34,:,i]=City_list[1:34]
        DoItAgain=lb.check2(Population[:,:,i],temporary)

Cost_Vector=lb.Cost_fun(Population,Population_size)
orderedPopulation, Cost_ordered=lb.Order(Population, Cost_Vector, City_numb, Population_size)


Prob_vector=0.25*np.ones(4) #probability vector for random search
Prob_vector=np.array([0.25, 0.25, 0.25, 0.25])
iteration_number=500
l2Vect=np.zeros(iteration_number+1)
l2Vect[0]=np.mean(Cost_ordered[0:50])


for i in range(iteration_number):  ##how to do a random search
    new_Population=np.zeros((City_numb,3,Population_size))
    for j in range(Population_size):
        Selected=lb.selection(orderedPopulation, Population_size)
        Population_element=Selected
        action=np.random.choice(np.array([1,2,3,4]),p=Prob_vector)
        child=lb.genetic_mutation(Population_element, action, City_numb)
        DoItAgain=lb.check2(child,temporary)
        while DoItAgain==True:
            child=lb.genetic_mutation(Population_element, action, City_numb)
            DoItAgain=lb.check2(child,temporary)
             
        new_Population[:,:,j]=child
        
    
    Cost_vector=lb.Cost_fun(new_Population, Population_size)
    orderedPopulation, Cost_ordered= lb.Order(new_Population, Cost_vector, City_numb, Population_size)
    l2Vect[i+1]= np.mean(Cost_ordered[0])
    




fig,ax=plt.subplots(figsize=(10,10))
ax.scatter(temporary[:,1],temporary[:,2])
ax.plot(temporary[:,1],temporary[:,2])
np.save('randWorstCircle.npy',temporary)
np.save('randomL2vet.npy',l2Vect)
fig1,ax1=plt.subplots(figsize=(10,10))
ax1.scatter(orderedPopulation[:,1,0],orderedPopulation[:,2,0])
ax1.plot(orderedPopulation[:,1,0],orderedPopulation[:,2,0],color='red')
np.save('randomBest.npy',orderedPopulation)


