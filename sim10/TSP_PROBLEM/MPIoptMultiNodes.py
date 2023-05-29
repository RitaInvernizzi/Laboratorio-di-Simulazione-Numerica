# -*- coding: utf-8 -*-
"""
Created on Mon May 22 12:11:09 2023

@author: Rita
"""

import numpy as np
import library as lb
import matplotlib.pyplot as plt
import mpi4py 
from mpi4py import MPI


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

tstart = MPI.Wtime()
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
np.save('intPath.npy', orderedPopulation[:,:,0])

Prob_vector=0.25*np.ones(4) #probability vector for random search
Prob_vector=np.array([0.08, 0.08, 0.08, 0.08, 0.68])
iteration_number=200
l2Vect=np.zeros(iteration_number+1)
l2Vect[0]=np.mean(Cost_ordered[0:int(Population_size*0.5)])


for i in range(iteration_number):  ##how to do a random search
    new_Population=np.zeros((City_numb,3,Population_size))
    j=0
    while j<Population_size:
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
    best1 = orderedPopulation[:,:,0]
    best2 = orderedPopulation[:,:,0]
    
    
    
    if i == 100:
        print(i)
        n1=0
        n2=1
        
        
        if rank == n1:
            #controllo che n1 e n2 si scambino
            #faccio il print dell' elemento finale di n1
            print('I am node', n1 ,'the selected point is', best1[:,0])
            
            
            
             
        elif rank == n2:
             print('I am node', n2,'the selected point is:' , best2[:,0])
             
        
        
        if rank == n1: # il nodo n1 scambia con il nodo n2
           comm.Send(np.ascontiguousarray(best1), dest=n2)
           comm.Recv(np.ascontiguousarray(best2), source=n2)
           print('I am node', n1,'my new selected last point is:' , best2[:,0])
           orderedPopulation[:,:,0] = best2
         
        elif rank == n2: 
            comm.Recv(np.ascontiguousarray(best1), source=n1)
            comm.Send(np.ascontiguousarray(best2), dest=n1)
            print('I am node', n2,'my new selected last point is:' ,best1[:,0] )
            orderedPopulation[:,:,0] = best1
        
        
       

"""if rank == 0:
    np.save('BestPath1.npy', orderedPopulation[:,:,0])
    np.save('L2_1.npy', l2Vect)


if rank == 1:
    np.save('BestPath2.npy', orderedPopulation[:,:,0])
    np.save('L2_2.npy', l2Vect)"""


 

tend= MPI.Wtime()
print(tend-tstart)
MPI.Finalize()