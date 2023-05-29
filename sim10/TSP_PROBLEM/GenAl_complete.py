# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 12:05:12 2023

@author: Rita
"""

import numpy as np
import library as lb
import matplotlib.pyplot as plt
import time

start = time.time()

City_numb = 50
Population_size = 100



City_list=np.empty((City_numb,3))
temporary=np.empty((City_numb,3))
data = np.loadtxt( 'American_capitals.dat', skiprows= 0, usecols=[2,3])
text_file = open("American_capitals.dat", "r")
#read whole file to a string
names = text_file.read()
#close file
text_file.close()
#print(names)

for i in range(City_numb):
    City_list[i,:]=np.array([i,data[i,0],data[i,1]])
    temporary[i,:]=temporary[i,:]=City_list[i,:]
    

Population=np.empty((City_numb,3,Population_size))



for i in range(Population_size): #generate population
    Population[0,:,i]=np.array([temporary[0,0],temporary[0,1],temporary[0,2]])
    np.random.shuffle(City_list[1:City_numb])
    Population[1:City_numb,:,i]=City_list[1:City_numb]
    #apply check
    DoItAgain=lb.check2(Population[:,:,i],temporary)
    while DoItAgain==True:
        np.random.shuffle(City_list[1:City_numb])
        Population[1:City_numb,:,i]=City_list[1:City_numb]
        DoItAgain=lb.check2(Population[:,:,i],temporary)





Cost_Vector=lb.Cost_fun(Population,Population_size)
orderedPopulation, Cost_ordered=lb.Order(Population, Cost_Vector, City_numb, Population_size)


Prob_vector=0.25*np.ones(4) #probability vector for random search
Prob_vector=np.array([0.08, 0.08, 0.08, 0.08, 0.68])
iteration_number=200
l2Vect=np.zeros(iteration_number+1)
l2Vect[0]=np.mean(Cost_ordered[0:int(Population_size*0.5)])


for i in range(iteration_number):  ##how to do a random search
    new_Population=np.zeros((City_numb,3,Population_size))
    j=0
    while j<Population_size:
        
        #Population_element=orderedPopulation[:,:,j]
        action=np.random.choice(np.array([1,2,3,4,5]),p=Prob_vector)

        
        if action==5:
            #select mom and dad
            Mom=lb.selection(orderedPopulation,Population_size)
            Dad=lb.selection(orderedPopulation,Population_size)
            child1, child2= lb.cross_over(Mom, Dad, City_numb)
            DoItAgain1=lb.check2(child1,temporary)
            DoItAgain2=lb.check2(child2,temporary)
            
            while DoItAgain1==True & DoItAgain2==True:
                child1, child2= lb.cross_over(Mom, Dad, City_numb)
                DoItAgain1=lb.check2(child1,temporary)
                DoItAgain2=lb.check2(child2,temporary)
            
            new_Population[:,:,j]=child1
            if j==Population_size-1:
               break
            else: 
                j=j+1
                new_Population[:,:,j]=child2
            
        else:
            
            Population_element=lb.selection(orderedPopulation,Population_size)
            child=lb.genetic_mutation(Population_element, action, City_numb)
            DoItAgain=lb.check2(child,temporary)
            while DoItAgain==True:
                child=lb.genetic_mutation(Population_element, action, City_numb)
                DoItAgain=lb.check2(child,temporary)
                 
            new_Population[:,:,j]=child
            if j==Population_size-1:
                break
            else:
                j=j+1
            
            
            
            
            
            
        
        
    
    Cost_vector=lb.Cost_fun(new_Population, Population_size)
    orderedPopulation, Cost_ordered= lb.Order(new_Population, Cost_vector, City_numb, Population_size)
    l2Vect[i+1]= np.mean(Cost_ordered[0:int(Population_size*0.5)])
    
end = time.time()

print(end - start)


np.save('L2_square1.npy',l2Vect) 
np.save('Worst_square1.npy', temporary)  
np.save('Best_square1.npy',orderedPopulation )
    
    
fig,ax=plt.subplots(figsize=(10,10))
ax.scatter(temporary[:,1],temporary[:,2])
ax.plot(temporary[:,1],temporary[:,2])

fig1,ax1=plt.subplots(figsize=(10,10))
ax1.scatter(orderedPopulation[:,1,0],orderedPopulation[:,2,0])
ax1.plot(orderedPopulation[:,1,0],orderedPopulation[:,2,0],color='red')
    

