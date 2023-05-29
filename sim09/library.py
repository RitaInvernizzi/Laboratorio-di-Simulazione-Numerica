# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 18:08:55 2023

@author: Rita
"""

import numpy as np
#import matplotlib.pyplot as plt

#Cities are organised on a circle 
#random.shuffle()
#write a check operator

def Cost_fun(Population,N):
    """return the lenght, aka the cost, of a route in l2 norm"""
    cost=np.zeros(N) #it is a vector and N is the size of the population
    for i in range(N):
        Route=Population[:,:,i]
        cost[i]=(np.power(Route[len(Route)-1,1]-Route[0,1],2)+np.power(Route[len(Route)-1,2]-Route[0,2],2))
        
        c=0
        for j in range(len(Route)-1):
            x2=np.power(Route[j+1,1]-Route[j,1],2)
            y2=np.power(Route[j+1,2]-Route[j,2],2)
            c += (x2+y2)
            
        cost[i]= cost[i]+c
            
    return cost


def Order(Population, Cost_vector, City_numb,Population_size):
    Population_ranked=np.zeros((City_numb,3,Population_size))
    Cost_ordered=np.zeros(Population_size)
    temp=Cost_vector
    Cost_ordered=np.sort(Cost_vector)
    for i in range(Population_size):
        index=np.where(temp==Cost_ordered[i])
        Population_ranked[:,:,i]=Population[:,:,index[0][0]]
    
    return Population_ranked, Cost_ordered

def selection(Population, Population_size):
    """operartor that gives the possibility of selecting a certain element
       of the population, once it has been ranked"""
    selection_index=int(Population_size*np.power(np.random.rand(),4))
    
    Selected=Population[:,:,selection_index]
    return Selected
    
    
def genetic_mutation(Population_element, do, City_numb):
    """if do=1 pair permutation
          do=2 shift of n positions of m contiguous cities
          do=3 permutation of m contiguous cities with other m contiguous
          do=4 inversion of order of m contiguous cities
          population_element is the one you get after applying the selection operator"""
    
    if do==1:
        child=np.zeros((City_numb,3))
        #index=np.random.randint(1,City_numb-2)
        index=np.random.randint(1,City_numb-1)
        a=Population_element[index,:]
        b=Population_element[index+1,:]
        if index+1==City_numb-1:
            child[index,:]=b
            child[index+1,:]=a
            child[0,:]=Population_element[0,:]
            child[1:index,:]=Population_element[1:index,:]
        else:
            child[index,:]=b
            child[index+1,:]=a
            child[0,:]=Population_element[0,:]
            child[1:index,:]=Population_element[1:index,:]
            child[index+2:City_numb,:]=Population_element[index+2:City_numb,:]
            

    elif do==2:
        child=np.zeros((City_numb,3))
        start=np.random.randint(1,City_numb-3) #starting point of the shift
        m=np.random.randint(1,City_numb-1-start) #number of cities i want to shift
        end=start+m-1
        n=np.random.randint(1,City_numb-end-1)# entity of the shift
        cut=Population_element[start:end+1,:]
        child[0,:]=Population_element[0,:]
        child[(start+n):(end+1+n),:]=cut
        if end+n==(City_numb-1):
            fin_ind=len(Population_element[end+1:City_numb-n])
            child[1:fin_ind,:]=Population_element[end+1:City_numb,:]
            child[fin_ind:start+n,:]=Population_element[1:start,:]
            #the cities have been shifted up to the end of the vector
        else:
        
            child[end+1+n:City_numb,:]=Population_element[end+1:City_numb-n,:]
            fin_ind=len(Population_element[City_numb-n-1:City_numb])
            child[1:fin_ind,:]=Population_element[City_numb-n:City_numb,:]
            child[fin_ind:start+n,:]=Population_element[1:start,:]
            
    elif do==3: #rifare questo
        x=Population_element
        child=np.zeros((City_numb,3))
        start=np.random.randint(1,City_numb-3)
        #print(start)
        p=np.random.randint(1,int((-start+City_numb+1)*0.5))
        #print(p)
        end=2*int(p)+start
        #print(end)
        medium=(end-start)*0.5+start
        medium=int(medium)
        #print(medium)
        a=Population_element[start:medium+1,:]
        #print(a)
        b=Population_element[medium+1:end+1,:]
        #print(b)
        child[0,:]=x[0,:]
        child[1:start,:]=x[1:start,:]
        child[start:medium,:]=b
        child[medium:end+1,:]=a
        child[end+1:City_numb,:]=x[end+1:City_numb,:]
        
    else:
        child=np.zeros((City_numb,3))
        start=np.random.randint(1,City_numb)
        end=np.random.randint(3,City_numb)
        z=Population_element[start:end+1,:]
        z=z[::-1]
        Population_element[start:end+1,:]=z
        child=Population_element
        
    return child
    
def cross_over(Mom, Dad, City_numb):
    children1=np.zeros((City_numb,3))
    children2=np.zeros((City_numb,3))
    n=np.random.randint(1,City_numb-2)
    children1[0:n,:]=Mom[0:n,:]
    children2[0:n,:]=Dad[0:n,:]
    mom_side= Mom[n:City_numb,:]
    dad_side= Dad[n:City_numb,:]
    q=len(mom_side)
    vect1=np.zeros(q)
    vect2=np.zeros(q)
    
    
    for i in range(q):
        index1=np.where(Dad[:,0]==mom_side[i,0])
        vect1[i]=index1[0][0]
        index2=np.where(Mom[:,0]==dad_side[i,0])
        vect2[i]=index2[0][0]
        
    vect1=np.sort(vect1)#dad's positions
    vect2=np.sort(vect2)#mom's positions
    #fill1 & fill2 
    
    for j in range(q):
        
        children1[j+n,:]=Dad[int(vect1[j]),:]
        children2[j+n,:]=Mom[int(vect2[j]),:]
        
    return children1, children2


def check1(Population_element, Temporary):
    if Population_element[0,:,:]==Temporary[0,:,:]:
        return False
    else:
        return True
    
def check2(Population_element, Temporary):
    index0=np.zeros(len(Temporary))
    index1=np.zeros(len(Temporary))
    DoItAgain=False
    for i in range(len(Temporary)):
        index0[i]=Population_element[i,0]
        index1[i]=Temporary[i,0]
    flag=0
    j=0
    while flag==0 & j<len(Temporary):
        control=np.where(index0==Temporary[j])
        if len(control[0])>=2 or len(control[0]==0):
            DoItAgain=True
            flag=1
        else:
            j = j+1
            if j==len(Temporary):
                break
            
    return DoItAgain
        
            
    
    
    

    

