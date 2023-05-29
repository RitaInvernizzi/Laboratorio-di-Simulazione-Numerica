# -*- coding: utf-8 -*-
"""
Created on Thu May 25 11:17:16 2023

@author: Rita
"""

"""
Created on Mon May 22 18:02:20 2023

@author: Rita
"""


import numpy as np
import matplotlib.pyplot as plt
import MyFunctions as mf

def Psi(x, mu, sigma): #Psi^2
    A= np.exp(-((x-mu)**2)/(2*sigma**2))
    B= np.exp(-((x+mu)**2)/(2*sigma**2))
    C= 2*A*B
    return A+B+C


def set_limits(mu,sigma):
    """funzione che limita l'esplorazione su un range limitato per mu e sigma  """
    mu = min(max(0.70,mu),0.99)
    
    sigma = min(max(0.50, sigma ),0.7)
    return mu, sigma

def Energy(x, mu, sigma):
    # funxione per il calcolo dell'energia
    tot_energy = 0
    h_bar = 1
    m = 1
    A = np.exp(-((x-mu)**2)/(2*sigma**2))
    B = np.exp(-((x+mu)**2)/(2*sigma**2))
    psi_trial = A+B
    V = np.power(x, 4) - 2.5 * np.power(x, 2)
    kin_psi = -(h_bar / (2 * m)) * (1. / np.power(sigma, 2)) * (np.exp(-np.power((x - mu), 2) / (2 * np.power(sigma, 2))) * ((np.power(x - mu, 2) / np.power(sigma, 2)) - 1) + np.exp(-np.power((x + mu), 2) / (2 * np.power(sigma, 2))) * ((np.power(x + mu, 2) / np.power(sigma, 2)) - 1))
    pot_psi = V*psi_trial
    tot_energy = (kin_psi + pot_psi)/psi_trial
	
    return tot_energy

def Segno(): #funzione che definisce la direzione del passo
    ind= np.random.rand()
    a=0
    if ind>=0.5:
       a=+1
    else:
        a=-1
    return a

def Metropolis(x0, step, mu, sigma): 
    
    x= Segno()*step*np.random.rand()+x0 #genero le nuove coordinate estraendo da una prob uniforme
    A= Psi(x,mu,sigma)/Psi(x0,mu,sigma)
    alpha= min(1,A)
    r= np.random.rand()
    
    if r<=alpha:
       x1=x
    else:
        x1=x0
    return x1




def variational_monte_carlo(x0, sigma, mu, delta, num_steps, num_blocks):
    x = x0
    energies = []
    energies2 = []
    for block in range(num_blocks):
        energy_sum = 0
        for step in range(num_steps):
            
            x = Metropolis(x, delta, mu, sigma)
            energy_sum += Energy(x, mu, sigma)
            
        energy = energy_sum / num_steps
        energy2 = energy*energy
        energies.append(energy)
        energies2.append(energy2)
        last_conf = x
        
        
    return energies, energies2, last_conf


def energy_function(sigma, mu, last_conf):
    
    E = Energy(last_conf, mu, sigma)
    return E


def simulated_annealing(x0, sigma0, mu0, delta, num_steps, num_blocks, initial_temp, temp_update):
    x = x0
    sigma = sigma0
    mu = mu0
    temp = initial_temp
    
    parameters =[]
    sa_steps= 100
    energies = np.zeros((sa_steps,num_blocks))
    energies2 = np.zeros((sa_steps,num_blocks))
    Ene = []
    Ene2 =[]
    
    for i in range(sa_steps):
        energy,energy2, last_conf = variational_monte_carlo(x, sigma, mu, delta, num_steps, num_blocks)
        energies[i,:] = energy
        energies2[i,:] = energy2
        
        parameters.append((sigma, mu))
        new_sigma = sigma + np.random.uniform(-delta, delta)*0.25
        new_mu = mu + np.random.uniform(-delta, delta)*0.25
        new_mu, new_sigma = set_limits(new_mu, new_sigma)
        current_ene = energy_function(mu, sigma, last_conf)
        new_ene=energy_function(new_mu, new_sigma, last_conf)
        Ene.append(current_ene)
        Ene2.append(current_ene*current_ene)
        energy_diff = new_ene - current_ene
        if energy_diff < 0 or np.random.uniform(0, 1) < np.exp(-energy_diff / temp):
            sigma = new_sigma
            mu = new_mu
        
        if i%10 == 0:
            temp *= temp_update 
            
    return energies, parameters


num_steps = 100
num_blocks = 100
x0 = 0.0
delta = 0.1
initial_temp = 10.0
temp_update = 0.9



initial_sigma = 0.55
initial_mu = 0.98
energies, parameters = simulated_annealing(x0,initial_sigma, initial_mu, delta,num_steps, num_blocks, initial_temp, temp_update)
sa_steps = 100
num_samples = sa_steps
Ene = energies[:,num_blocks-1]
Ene2 = np.power(energies[:,num_blocks-1],2)

m_ene, error_m_ene = mf.BlockMean(Ene, Ene2, sa_steps)
plt.errorbar(range(num_samples), m_ene, yerr=error_m_ene, fmt='o')
plt.xlabel("Number SA steps")
plt.ylabel("⟨Ĥ⟩")
plt.title("Estimation of ⟨Ĥ⟩ and its statistical uncertainty vs. SA steps")
plt.show()

param = np.asarray(parameters)
np.save('param.npy', param)
np.save('sa_ene.npy',m_ene)
np.save('err_mene_sa.npy',error_m_ene)




def variational_monte_carlo1(x0, sigma, mu, delta, num_steps, num_blocks):
    x = x0
    energies = []
    energies2 =[]
    configurations = []
    for block in range(num_blocks):
        energy_sum = 0
        block_configurations = []
        for step in range(num_steps):
            x=Metropolis(x, delta, mu, sigma)
            energy_sum += Energy(x, mu, sigma)
            block_configurations.append(x)
        
        energy = energy_sum / num_steps
        energy2 = energy*energy
        energies.append(energy)
        energies2.append(energy2)
        configurations.extend(block_configurations)
    
    return energies , energies2, configurations

index1 = np.where(m_ene==np.min(m_ene))
mu = parameters[index1[0][0]][1]
sigma = parameters[index1[0][0]][0]
num_blocks = 100
num_steps = 5000

x0 = 0.0
# Run the variational Monte Carlo simulation
EneMC, EneMC2, configurations = variational_monte_carlo1(x0, sigma, mu, delta, num_steps, num_blocks)

# Plot the histogram of the sampled configurations
plt.hist(configurations, bins='auto', density=True)
plt.xlabel("Configuration")
plt.ylabel("Frequency")
plt.title("Histogram of Sampled Configurations")
plt.show()
conf = np.asarray(configurations)
np.save('conf.npy', conf)

mean1, error1, = mf.BlockMean(EneMC, EneMC2, 100)
plt.errorbar(range(100), mean1, yerr=error1, fmt='o')
plt.axhline(y=-0.46, color = 'red', label='reference value')
plt.xlabel("Number MC steps")
plt.ylabel("⟨Ĥ⟩")
plt.title("Estimation of ⟨Ĥ⟩ and its statistical uncertainty")
plt.legend()
plt.show()

np.save('EnMC.npy', mean1)
np.save('errorEnMC.npy', error1)
