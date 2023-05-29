# -*- coding: utf-8 -*-
"""
Created on Fri May 26 00:33:06 2023

@author: Rita
"""

import numpy as np
import library as lb
import matplotlib.pyplot as plt
import mpi4py 
from mpi4py import MPI

#Population/Population ordered : contiene 100 matrici 50*3, che indicano i varii percorsi possibili. 
# Nella matrice 50*3 la prima colonna indica l'indeice della città

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

names = text_file.read()

text_file.close()


for i in range(City_numb):
    City_list[i,:]=np.array([i,data[i,0],data[i,1]])
    temporary[i,:]=temporary[i,:]=City_list[i,:]
    

Population=np.empty((City_numb,3,Population_size))


 #generate population
for i in range(Population_size):
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
Prob_vector=np.array([0.08, 0.08, 0.08, 0.08, 0.68])# probabilità per GA search
##################################################################
###############################################################
iteration_number=10 ## NUMERO di GENERAZIONI
#################################################
#################################################
l2Vect=np.zeros(iteration_number+1) # vettore per salvare la cost function
l2Vect[0]=np.mean(Cost_ordered[0:int(Population_size*0.5)])


for i in range(iteration_number): 
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
    # salva la nuova popolazione e ordinala
    Cost_vector=lb.Cost_fun(new_Population, Population_size)
    orderedPopulation, Cost_ordered= lb.Order(new_Population, Cost_vector, City_numb, Population_size)
    l2Vect[i+1]= np.mean(Cost_ordered[0:int(Population_size*0.5)])
    
    if i%10 == 0:
        print('This is the generation:', i)
       
        
        n1 = 0 # nodo zero
        n2 = 1 # nodo uno
    
    
        # inizializzare vettori specchio per i nodi
        
        
        if rank == n1:
            print('node',rank)
            print('I am the best path for node', rank)
            print(orderedPopulation[:,0,0])
            print('*---------------------*')
            
            BoxA = orderedPopulation
            BoxB = orderedPopulation
            
            
        elif rank == n2:
            
            print('node',rank)
            print('I am the best path for node', rank)
            print(orderedPopulation[:,0,0])
            print('*------------------------*')
            BoxB = orderedPopulation
            BoxA = orderedPopulation
            
       
            
        
        if rank == n1: # inviare e ricevere la lista degli indici delle città
            print('node', rank, 'sends',BoxA[:,0,0], 'to', n2 )
            comm.Send(np.ascontiguousarray(BoxA[:,0,0]), dest=n2)
            comm.Recv(np.ascontiguousarray(BoxB[:,0,0]), source=n2)
            print('node', rank, 'receives',BoxB[:,0,0], 'from', n2)
            
        elif rank == n2:
            print('node', rank, 'receives',BoxA[:,0,0], 'from',n1)
            comm.Recv(np.ascontiguousarray(BoxA[:,0,0]), source=n1)
            comm.Send(np.ascontiguousarray(BoxB[:,0,0]), dest=n1)
            print('node', rank, 'sends',BoxA[:,0,0], 'to',n1)
        
        
        if rank == n1:
           
            comm.Send(np.ascontiguousarray(BoxA[:,1,0]), dest=n2)
            comm.Recv(np.ascontiguousarray(BoxB[:,1,0]), source=n2)
        
        elif rank == n2:
            comm.Recv(np.ascontiguousarray(BoxA[:,1,0]), source=n1)
            comm.Send(np.ascontiguousarray(BoxB[:,1,0]), dest=n1)
        
        
        if rank == n1:
            comm.Send(np.ascontiguousarray(BoxA[:,2,0]), dest=n2)
            comm.Recv(np.ascontiguousarray(BoxB[:,2,0]), source=n2)
        
        elif rank == n2:
            comm.Recv(np.ascontiguousarray(BoxA[:,2,0]), source=n1)
            comm.Send(np.ascontiguousarray(BoxB[:,2,0]), dest=n1)
            
    

tend= MPI.Wtime()
print(tend-tstart)
MPI.Finalize()