# -*- coding: utf-8 -*-
"""
Created on Mon May 22 14:17:47 2023

@author: Rita
"""

import numpy as np

import matplotlib.pyplot as plt

init_path = np.load('intPath.npy')

fig1 = plt.subplots(figsize= (15,10))
plt.title('Initial path')
plt.plot(init_path[:,1], init_path[:,2])
plt.scatter(init_path[:,1], init_path[:,2])
plt.grid('True')



path = np.load('BestPath1.npy')

fig2 = plt.subplots(figsize= (15,10))
plt.title('Final path: node 1')
plt.plot(path[:,1], path[:,2])
plt.scatter(path[:,1], path[:,2],color ='red')
plt.grid('True')


cost = np.load('L2_1.npy')
fig4 = plt.subplots(figsize= (15,10))
plt.title('Cost Function: node 1')
plt.plot(np.arange(len(cost)),cost,'*', color='green')
plt.grid('True')







path = np.load('BestPath2.npy')
fig3 = plt.subplots(figsize= (15,10))
plt.title('Final path: node 2')
plt.plot(path[:,1], path[:,2])
plt.scatter(path[:,1], path[:,2],color ='red')
plt.grid('True')


cost = np.load('L2_2.npy')
fig5 = plt.subplots(figsize= (15,10))
plt.title('Cost Function: node 2')
plt.plot(np.arange(len(cost)),cost, '*', color='green')
plt.grid('True')



path = np.load('BestPathSingleNode.npy')
fig6 = plt.subplots(figsize= (15,10))
plt.title('Final path: Single node')
plt.plot(path[:,1], path[:,2])
plt.scatter(path[:,1], path[:,2],color ='red')
plt.grid('True')


cost = np.load('L2_SingleNode.npy')
fig6 = plt.subplots(figsize= (15,10))
plt.title('Cost Function: single node')
plt.plot(np.arange(len(cost)),cost, '*', color='green')
plt.grid('True')


fig7= plt.subplots(figsize=(15,10))
cost = np.load('L2_SingleNode.npy')
plt.title('Cost Function: up to 10 parallel GA searches')
plt.plot(np.arange(len(cost)),cost, '--',  label = 'Single node')
cost = np.load('L2_1.npy')
plt.plot(np.arange(len(cost)),cost, '--',  label = 'node1')
cost = np.load('L2_2.npy')
plt.plot(np.arange(len(cost)),cost, '--', label = 'node2')
cost = np.load('L2_3.npy')
plt.plot(np.arange(len(cost)),cost, '--', label = 'node3')
cost = np.load('L2_4.npy')
plt.plot(np.arange(len(cost)),cost, '--',  label = 'node4')
"""
cost = np.load('L2_5.npy')
plt.plot(np.arange(len(cost)),cost, '*',  label = 'node5')
cost = np.load('L2_6.npy')
plt.plot(np.arange(len(cost)),cost, '*',  label = 'node6')
cost = np.load('L2_7.npy')
plt.plot(np.arange(len(cost)),cost, '*',  label = 'node7')
cost = np.load('L2_8.npy')
plt.plot(np.arange(len(cost)),cost, '*', label = 'node8')
cost = np.load('L2_9.npy')
plt.plot(np.arange(len(cost)),cost, '*',  label = 'node9')
cost = np.load('L2_10.npy')
plt.plot(np.arange(len(cost)),cost, '*',  label = 'node10')"""
plt.legend()
plt.grid('True')


"""fig8 = plt.subplots(figsize=(15,10))
plt.title('Cost Function: 10 parallel GA searches')
plt.plot(np.arange(len(cost)),cost, '--',  label = 'Single node')
cost = np.load('L2_8.npy')
plt.plot(np.arange(len(cost)),cost, '--', label = 'node8')
plt.legend()
plt.grid('True')"""