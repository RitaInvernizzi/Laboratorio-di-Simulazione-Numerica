# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 14:56:10 2022

@author: Rita
"""

# libreria di funzioni utili
import numpy as np
import math
import numba
import MyFunctions as MF
np.random.seed(0)
def PsiOne(x,y,z): # gs, è già il mod^2  di psi
    r= math.sqrt(x**2 + y**2 + z**2)
    return math.exp(-2*r)/math.pi

def PsiTwo(x,y,z): # primo stato eccitato
    r= math.sqrt(x**2 + y**2 + z**2)
    return (r**2)*math.exp(-r)/(math.pi*32)*np.power(np.cos(np.arctan2(y,x)),2)

def Segno(): #funzione che definisce la direzione del passo
    ind= np.random.rand()
    a=0
    if ind>=0.5:
       a=+1
    else:
        a=-1
    return a

def Metropolis(x0, y0,z0, step, choice): 
    x= Segno()*step*np.random.rand()+x0 #genero le nuove coordinate estraendo da una prob uniforme
    y= Segno()*step*np.random.rand()+y0
    z= Segno()*step*np.random.rand()+y0
    if choice == 0:
       A= PsiOne(x,y,z)/PsiOne(x0, y0,z0)
    else:
         A= PsiTwo(x,y,z)/PsiTwo(x0, y0,z0)
         
    alpha= min(1,A)
    r= np.random.rand();
    if r<=alpha:
       x1=x
       y1=y
       z1=z
    else:
        x1=x0
        y1=y0
        z1=z0
    return x1, y1, z1, alpha


#definisco l'origine 
np.random.seed=0
x0=0 # questi li scelgo come i massimo delle due distribuzioni di probabilità
y0=0
a=0.0529
z0=math.sqrt(1/2)/a #scrivo le lunghezze in unità di raggio di bohr
step=1.1 #lo scelgo in modo da avere una probabilià di accettazione di 0.5
choice=0 # studio lo stato fondamentale

M=1000000
N= 100
Accept=np.zeros(M)
Radius= np.zeros(M)
a=x0
b=y0
c=z0
for i in range(M):
    x1,y1,z1,Accept[i]= Metropolis(a,b,c, step, choice)
    Radius[i]= math.sqrt(x1**2 + y1**2 +z1**2)
    a=x1
    b=y1
    c=z1



# implemento il data bloking
L=int(M/N)
acc1, err_acc1 = MF.SimpleMean(Accept,N,L) 
meanAcc1, err_meanAcc1 = MF.BlockMean(acc1, err_acc1,N)
np.save('AcceptanceGS.npy', meanAcc1, allow_pickle=True, fix_imports=True)
np.save('ErrorGS.npy', err_meanAcc1, allow_pickle=True, fix_imports=True)
M1,M2 =MF.SimpleMean(Radius,N,L)
# raggio sf uniform
MeanRad, ErrorRad= MF.BlockMean(M1,M2,N)
np.save('radGSuniform.npy', MeanRad, allow_pickle=True, fix_imports=True)
np.save('ErrorGSuniform.npy', ErrorRad, allow_pickle=True, fix_imports=True)
# faccio la stessa cosa campionando da una gaussiana
def BoxMuller():
    u1=np.sqrt(-2*np.log(np.random.rand()))*np.cos(2*np.pi*np.random.rand())
    return u1


def MetropolisGauss(x0, y0,z0, step, choice): 
    x= step*BoxMuller()+x0 #genero le nuove coordinate estraendo da una prob uniforme
    y= step*BoxMuller()+y0
    z= step*BoxMuller()+z0
    if choice == 0:
       A= PsiOne(x,y,z)/PsiOne(x0, y0,z0)
    else:
         A= PsiTwo(x,y,z)/PsiTwo(x0, y0,z0)
         
    alpha= min(1,A)
    r= np.random.rand();
    if r<=alpha:
       x1=x
       y1=y
       z1=z
    else:
        x1=x0
        y1=y0
        z1=z0
    return x1, y1, z1, alpha





# studio il problema scegliendo una gaussiana per fare i compionamenti
Accept1=np.zeros(M)
Radius1= np.zeros(M)
x0=0 # questi li scelgo come i massimo delle due distribuzioni di probabilità
y0=0
a=0.0529
z0=np.sqrt(0.5)/a #scrivo le lunghezze in unità di raggio di bohr
a=x0
b=y0
c=z0
step = 1.0

for i in range(M):
    x1,y1,z1,Accept1[i]= MetropolisGauss(a,b,c, step, choice)
    Radius1[i]= math.sqrt(x1**2 + y1**2 +z1**2)
    a=x1
    b=y1
    c=z1


# implemento il data bloking

M1G,M2G =MF.SimpleMean(Radius1,N,L)

MeanRadG, ErrorRadG= MF.BlockMean(M1G,M2G,N)
# raggio sf Gauss
np.save('radGSgauss.npy', MeanRadG, allow_pickle=True, fix_imports=True)
np.save('ErrorGSgauss.npy', ErrorRadG, allow_pickle=True, fix_imports=True)


# Studio del primo stato eccitato capionando con una gaussiana
M=1000000
N= 100
L= int(M/N)
Accept2=np.zeros(M)
Radius2= np.zeros(M)
choice2=1

x0=0 # questi li scelgo come i massimo delle due distribuzioni di probabilità
y0=0
a=0.0529
z0=math.sqrt(1/2)/a #scrivo le lunghezze in unità di raggio di bohr
a=x0
b=y0
c=z0
step=3.20
for i in range(M):
    x1,y1,z1,Accept2[i]= MetropolisGauss(a,b,c, step, choice2)
    Radius2[i]= math.sqrt(x1**2 + y1**2 +z1**2)
    a=x1
    b=y1
    c=z1


   
# implemento il data bloking

M1G_first,M2G_first =MF.SimpleMean(Radius2,N,L)
MeanRadG_first, ErrorRadG_first= MF.BlockMean(M1G_first,M2G_first,N)
# raggio sf Gauss
np.save('radFirstgauss.npy', MeanRadG_first, allow_pickle=True, fix_imports=True)
np.save('ErrorFirstgauss.npy', ErrorRadG_first, allow_pickle=True, fix_imports=True)

# Primo  stato eccitato campiono da una distribuzione uniforme
Accept3=np.zeros(M)
Radius2= np.zeros(M)


x0=0 # questi li scelgo come i massimo delle due distribuzioni di probabilità
y0=0
a=0.0529
z0=math.sqrt(1/2)/a #scrivo le lunghezze in unità di raggio di bohr
a=x0
b=y0
c=z0
step=3.20
choice2 = 2.0
Radius2= np.zeros(M)
for i in range(M):
    x1,y1,z1,Accept3[i]= Metropolis(a,b,c, step, choice2)
    Radius2[i]= math.sqrt(x1**2 + y1**2 +z1**2)
    a=x1
    b=y1
    c=z1



acc2, err_acc2 = MF.SimpleMean(Accept3,N,L) 
meanAcc2, err_meanAcc2 = MF.BlockMean(acc2, err_acc2,N)
np.save('AcceptanceFirst.npy', meanAcc2, allow_pickle=True, fix_imports=True)
np.save('ErrorFirst.npy', err_meanAcc2, allow_pickle=True, fix_imports=True)
# implemento il data bloking

M1_Uniformfirst,M2_Uniformfirst =MF.SimpleMean(Radius2,N,L)
MeanRadUniform_first, ErrorRadUniform_first= MF.BlockMean(M1_Uniformfirst,M2_Uniformfirst,N)
# raggio sf Gauss
np.save('radFirstUniform.npy', MeanRadUniform_first, allow_pickle=True, fix_imports=True)
np.save('ErrorFirstUniform.npy', ErrorRadUniform_first, allow_pickle=True, fix_imports=True)


#MOSTRO COSA SUCCEDE SE PARTO LONTANO DALL'ORIGINE: stato fondamentale e distri
# buzione uniforme


x0=200 # questi li scelgo come i massimo delle due distribuzioni di probabilità
y0=200
z0=200 #scrivo le lunghezze in unità di raggio di bohr
step=1.1 #lo scelgo in modo da avere una probabilià di accettazione di 0.5
choice=0 # studio lo stato fondamentale

M=1000000
N= 100
L = int(M/N)
Accept=np.zeros(M)
Radius= np.zeros(M)
a=x0
b=y0
c=z0
for i in range(M):
    x1,y1,z1,Accept[i]= Metropolis(a,b,c, step, choice)
    Radius[i]= math.sqrt(x1**2 + y1**2 +z1**2)
    a=x1
    b=y1
    c=z1
    
TryM1, TryM2 =MF.SimpleMean(Radius,N,L)
# raggio sf uniform: diverse CI
MeanRad_try, ErrorRad_try= MF.BlockMean(TryM1,TryM2,N)
np.save('Try.npy', MeanRad_try, allow_pickle=True, fix_imports=True)
np.save('ErrorTry.npy', ErrorRad_try, allow_pickle=True, fix_imports=True)