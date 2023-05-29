/****************************************************************
*****************************************************************
    _/    _/  _/_/_/  _/       Numerical Simulation Laboratory
   _/_/  _/ _/       _/       Physics Department
  _/  _/_/    _/    _/       Universita' degli Studi di Milano
 _/    _/       _/ _/       Prof. D.E. Galli
_/    _/  _/_/_/  _/_/_/_/ email: Davide.Galli@unimi.it
*****************************************************************
*****************************************************************/

#include <iostream>
#include <fstream>
#include <ostream>
#include <cmath>
#include <iomanip>
#include "Monte_Carlo_ISING_1D.h"


// restart variabile per equilibrazione
using namespace std;

int main()
{ 
  Input(); //Inizialization
  for(int iblk=1; iblk <= nblk; ++iblk) //Simulation
  {
    Reset(iblk);   //Reset block averages
    for(int istep=1; istep <= nstep; ++istep)
    {
      Move(metro);
      Measure();
      Accumulate(); //Update block averages
    }
    Averages(iblk);   //Print results for current block
  }
  ConfFinal(); //Write final configuration

  return 0;
}


void Input(void)
{
  ifstream ReadInput;
  ifstream ReadConf;

  cout << "Classic 1D Ising model             " << endl;
  cout << "Monte Carlo simulation             " << endl << endl;
  cout << "Nearest neighbour interaction      " << endl << endl;
  cout << "Boltzmann weight exp(- beta * H ), beta = 1/T " << endl << endl;
  cout << "The program uses k_B=1 and mu_B=1 units " << endl;

//Read seed for random numbers
   int p1, p2;
   ifstream Primes("Primes");
   Primes >> p1 >> p2 ;
   Primes.close();

   ifstream input("seed.in");
   input >> seed[0] >> seed[1] >> seed[2] >> seed[3];
   rnd.SetRandom(seed,p1,p2);
   input.close();
  
//Read input informations
  ReadInput.open("input.dat");
  ReadInput >> restart;
  
  ReadInput >> temp;
  beta = 1.0/temp;
  cout << "Temperature = " << temp << endl;

  ReadInput >> nspin;
  cout << "Number of spins = " << nspin << endl;

  ReadInput >> J;
  cout << "Exchange interaction = " << J << endl;

  ReadInput >> h;
  cout << "External field = " << h << endl << endl;
    
  ReadInput >> metro; // if=1 Metropolis else Gibbs

  ReadInput >> nblk;

  ReadInput >> nstep;

  if(metro==1) cout << "The program perform Metropolis moves" << endl;
  else cout << "The program perform Gibbs moves" << endl;
  cout << "Number of blocks = " << nblk << endl;
  cout << "Number of steps in one block = " << nstep << endl << endl;
  ReadInput.close();


//Prepare arrays for measurements
  iu = 0; //Energy
  ic = 1; //Heat capacity
  im = 2; //Magnetization
  ix = 3; //Magnetic susceptibility
 
  n_props = 4; //Number of observables

//initial configuration

  if (restart == 0){
      cout << " Equilibration " << endl;
      for (int i=0; i<nspin; ++i)
  {
    if(rnd.Rannyu() >= 0.5) s[i] = 1;
    else s[i] = -1;
  }
  
  }
  
  else {
      cout << " Read Configuration from config.final " << endl;
      ReadConf.open("config.final");
      for ( int i = 0; i < nspin; i++){
           ReadConf >> s[i];
      }
      ReadConf.close();
  }
  
//Evaluate energy etc. of the initial configuration
  Measure();

//Print initial values for the potential energy and virial
  cout << "Initial energy = " << walker[iu]/(double)nspin << endl;
}


void Move(int metro)
{
  int o;
  double p, energy_old, energy_new, sm, A, z;
  double energy_up, energy_down;

  for(int i=0; i<nspin; ++i)
  {
  //Select randomly a particle (for C++ syntax, 0 <= o <= nspin-1)
    o = (int)(rnd.Rannyu()*nspin);
    sm = s[o];
    if(metro==1) //Metropolis sampling
    {
       energy_old = Boltzmann( sm, o);
       s_new[o] = - s[o]; // spin flip
       sm = s_new[o];
       energy_new = Boltzmann(sm,o);
       A = min(1.0, exp( -beta*(energy_new-energy_old)));
       if (A==1){
          s[o] = s_new[o];
          accepted++;
       }
       
       else {
           
           
           z = rnd.Rannyu();
           
           if (z<A){
              
              s[o] = s_new[o]; // accetta il nuovo stato di spin
              accepted++;
           
           }
           
           else {
                
                s[o] = s[o]; // rifiuta lo stato di spin
           
           }
       
       
       }
       
       attempted++;

    }
    else //Gibbs sampling
    {
        energy_up = Boltzmann(+1,o);
        energy_down = Boltzmann(-1,o);
        p = exp(-beta*energy_up)/(exp(-beta*energy_up) + exp(-beta*energy_down));
        z = rnd.Rannyu();
        if(p>z){
           s[o] = +1;
           accepted++;
        }
        else{
             s[o] = -1;
             accepted++;
        }
        
        attempted++;
    }
  }
}

double Boltzmann(int sm, int ip)
{
  double ene = -J * sm * ( s[Pbc(ip-1)] + s[Pbc(ip+1)] ) - h * sm;
  return ene;
}

void Measure()
{
  //int bin;
  double u = 0.0, m = 0.0;

//cycle over spins
  for (int i=0; i<nspin; ++i)
  {
     u += -J * s[i] * s[Pbc(i+1)] - 0.5 * h * (s[i] + s[Pbc(i+1)]);
     m += s[i]; // calcolo magnetizzazione
// INCLUDE YOUR CODE HERE
  }
  walker[iu] = u;
  walker[ic] = u*u;
  walker[im] = m;
  walker[ix] = m*m;

}


void Reset(int iblk) //Reset block averages
{
   
   if(iblk == 1)
   {
       for(int i=0; i<n_props; ++i)
       {
           glob_av[i] = 0;
           glob_av2[i] = 0;
       }
   }

   for(int i=0; i<n_props; ++i)
   {
     blk_av[i] = 0;
   }
   blk_norm = 0;
   attempted = 0;
   accepted = 0;
}


void Accumulate(void) //Update block averages
{

   for(int i=0; i<n_props; ++i)
   {
     blk_av[i] = blk_av[i] + walker[i];
   }
   blk_norm = blk_norm + 1.0;
}


void Averages(int iblk) //Print results for current block
{
    
   ofstream Ene, Heat, Mag, Chi;
   const int wd=12;
    
    cout << "Block number " << iblk << endl;
    cout << "Acceptance rate " << accepted/attempted << endl << endl;
    
    
    stima_u = blk_av[iu]/blk_norm/(double)nspin; //Energy
    stima_c = (beta*beta*(blk_av[ic]/blk_norm-pow(blk_av[iu]/blk_norm,2)))/(double)nspin; // C. termica
    stima_m = blk_av[im]/blk_norm/(double)nspin; // Magnetizzazione
    stima_x = beta * blk_av[ix]/ blk_norm/ (double)nspin; // Suscettività
    glob_av[iu] += stima_u;
    glob_av[ic] += stima_c;
    glob_av[im] += stima_m;
    glob_av[ix] += stima_x;
    
    glob_av2[iu] += stima_u*stima_u;
    glob_av2[ic] += stima_c*stima_c;
    glob_av2[im] += stima_m*stima_m;
    glob_av2[ix] += stima_x*stima_x;
    
    err_u = Error(glob_av[iu], glob_av2[iu], iblk);
    err_c = Error(glob_av[ic], glob_av2[ic], iblk);
    err_m = Error(glob_av[im], glob_av2[im], iblk);
    err_x = Error(glob_av[ix], glob_av2[ix], iblk);
    
    
    // Collezionare i valori delle quantità di interesse post riequilibrazione 
    
    
    if (restart ==1){
        if (metro == 1){
            if ( temp == 0){
                Ene.open("out_metro.ene.dat",ios::app);
                Heat.open("out_metro.heat.dat",ios::app);
                Mag.open("out_metro.mag.dat",ios::app);
                Chi.open("out_metro.chi.dat",ios::app);
                
                Ene << setw(wd) << iblk << setw(wd) << temp << setw(wd) << stima_u << glob_av[iu] / (double)iblk << setw(wd) << err_u << endl;
                Heat << setw(wd) << iblk << setw(wd) << temp << setw(wd) << stima_c << glob_av[ic] / (double)iblk << setw(wd) << err_c << endl;
                Mag << setw(wd) << iblk << setw(wd) << temp << setw(wd) << stima_m << glob_av[im] / (double)iblk << setw(wd) << err_m << endl;
                Chi << setw(wd) << iblk << setw(wd) << temp << setw(wd) << stima_x << glob_av[ix] / (double)iblk << setw(wd) << err_x << endl;
                
            }
            
            else{
                Ene.open("out_metro.ene.h",ios::app);
                Heat.open("out_metro.heat.h",ios::app);
                Mag.open("out_metro.mag.h",ios::app);
                Chi.open("out_metro.chi.h",ios::app);
                
                Ene << setw(wd) << iblk << setw(wd) << temp << setw(wd) << stima_u << glob_av[iu] / (double)iblk << setw(wd) << err_u << endl;
                Heat << setw(wd) << iblk << setw(wd) << temp << setw(wd) << stima_c << glob_av[ic] / (double)iblk << setw(wd) << err_c << endl;
                Mag << setw(wd) << iblk << setw(wd) << temp << setw(wd) << stima_m << glob_av[im] / (double)iblk << setw(wd) << err_m << endl;
                Chi << setw(wd) << iblk << setw(wd) << temp << setw(wd) << stima_x << glob_av[ix] / (double)iblk << setw(wd) << err_x << endl;   
            }
        
        
        }
        
        else{
            
            
            if(temp==0){
                
                
                Ene.open("out_gibbs.ene.dat",ios::app);
                Heat.open("out_gibbs.heat.dat",ios::app);
                Mag.open("out_gibbs.mag.dat",ios::app);
                Chi.open("out_gibbs.chi.dat",ios::app);
                
                Ene << setw(wd) << iblk << setw(wd) << temp << setw(wd) << stima_u << glob_av[iu] / (double)iblk << setw(wd) << err_u << endl;
                Heat << setw(wd) << iblk << setw(wd) << temp << setw(wd) << stima_c << glob_av[ic] / (double)iblk << setw(wd) << err_c << endl;
                Mag << setw(wd) << iblk << setw(wd) << temp << setw(wd) << stima_m << glob_av[im] / (double)iblk << setw(wd) << err_m << endl;
                Chi << setw(wd) << iblk << setw(wd) << temp << setw(wd) << stima_x << glob_av[ix] / (double)iblk << setw(wd) << err_x << endl; 
            }
            
            else{
            
                Ene.open("out_gibbs.ene.h",ios::app);
                Heat.open("out_gibbs.heat.h",ios::app);
                Mag.open("out_gibbs.mag.h",ios::app);
                Chi.open("out_gibbs.chi.h",ios::app);
                
                Ene << setw(wd) << iblk << setw(wd) << temp << setw(wd) << stima_u << glob_av[iu] / (double)iblk << setw(wd) << err_u << endl;
                Heat << setw(wd) << iblk << setw(wd) << temp << setw(wd) << stima_c << glob_av[ic] / (double)iblk << setw(wd) << err_c << endl;
                Mag << setw(wd) << iblk << setw(wd) << temp << setw(wd) << stima_m << glob_av[im] / (double)iblk << setw(wd) << err_m << endl;
                Chi << setw(wd) << iblk << setw(wd) << temp << setw(wd) << stima_x << glob_av[ix] / (double)iblk << setw(wd) << err_x << endl; 
            }
            

        
        }
        
        
        Ene.close();
        Heat.close();
        Mag.close();
        Chi.close();
        
    
    }
    

// INCLUDE YOUR CODE HERE

    cout << "----------------------------" << endl << endl;
}


void ConfFinal(void)
{
  ofstream WriteConf;

  cout << "Print final configuration to file config.final " << endl << endl;
  WriteConf.open("config.final");
  for (int i=0; i<nspin; ++i)
  {
    WriteConf << s[i] << endl;
  }
  WriteConf.close();

  rnd.SaveSeed();
}

int Pbc(int i)  //Algorithm for periodic boundary conditions
{
    if(i >= nspin) i = i - nspin;
    else if(i < 0) i = i + nspin;
    return i;
}

double Error(double sum, double sum2, int iblk)
{
    if(iblk==1) return 0.0;
    else return sqrt((sum2/(double)iblk - pow(sum/(double)iblk,2))/(double)(iblk-1));
}

/****************************************************************
*****************************************************************
    _/    _/  _/_/_/  _/       Numerical Simulation Laboratory
   _/_/  _/ _/       _/       Physics Department
  _/  _/_/    _/    _/       Universita' degli Studi di Milano
 _/    _/       _/ _/       Prof. D.E. Galli
_/    _/  _/_/_/  _/_/_/_/ email: Davide.Galli@unimi.it
*****************************************************************
*****************************************************************/
