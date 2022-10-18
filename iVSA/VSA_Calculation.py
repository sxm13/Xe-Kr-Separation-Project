# Fit

import pyiast
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import pickle
import csv
from scipy.optimize import curve_fit

df_NAME=pd.read_excel("data.xlsx")
RESULT_NAME=""
for ZN in df_NAME["Filename"]:
    ZNN=str(ZN)
    df_Xe=pd.read_csv('../../Fit/Concat/'+ZNN+'_Xe.csv')
    df_Kr=pd.read_csv('../../Fit/Concat/'+ZNN+'_Kr.csv')
    f_list_tmp =['../../Fit/Concat/'+ZNN+'_Xe.csv','../../Fit/Concat/'+ZNN+'_Kr.csv']        
    df_ISO_list=[]        
    RESULT_NAME += f"{ZNN}\n"
    for f in f_list_tmp:
        df_tmp = pd.read_csv(f)
        df_ISO_list.append(df_tmp)
    iso_list = []
    g_difference_list= []
    for N in range(2): 
        try:
            iso_tmp = pyiast.ModelIsotherm(df_ISO_list[N],loading_key = 'q',
                                                   pressure_key = 'p',model = 'Quadratic')
            #pyiast.plot_isotherm(iso_tmp)
            iso_list.append(iso_tmp)
        except:
            try:
                iso_tmp = pyiast.ModelIsotherm(df_ISO_list[N],loading_key = 'q',
                                                   pressure_key = 'p',model = 'Langmuir')
                iso_list.append(iso_tmp)
            except:
                print(ZNN+"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    f_tmp = open('iso_'+ZNN+'_saved.bin','wb')
    pickle.dump(iso_list, f_tmp)
    f_tmp.close()
    f_tmp_new = open('iso_'+ZNN+'_saved.bin','rb')
    i_ISO_new = pickle.load(f_tmp_new)
    f_tmp_new.close()
    print('-------------------------------------------------')
    print(ZNN+'[[Loaded isotherm vairable for Xe,Kr]]')
    for i in range(len(i_ISO_new)):
          i_ISO_new[i].print_params()
    del iso_list[:]
    del g_difference_list[:]
    del f_list_tmp[:]
    del df_ISO_list[:]
print('-------------------------------------------------')
print('Calculated Adsorbent')
print('-------------------------------------------------')
print(RESULT_NAME)

# Calculate VSA

import time
import scipy.optimize as optim

df_NAME=pd.read_excel("data.xlsx")

bins_Xe = []
for nam in df_NAME["Filename"]:
    NAM=str(nam)
    f_tmp = open("iso_"+NAM+"_saved.bin",'rb')
    bin_tmp = pickle.load(f_tmp)
    bins_Xe.append(bin_tmp)
    f_tmp.close()
    
bins_Kr = []
for nam in df_NAME["Filename"]:
    NAM=str(nam)
    f_tmp = open("iso_"+NAM+"_saved.bin",'rb')
    bin_tmp = pickle.load(f_tmp)
    bins_Kr.append(bin_tmp)
    f_tmp.close()

Names_Kr=df_NAME["Filename"].to_numpy()
Name_list=Names_Kr
Names_Xe=df_NAME["Filename"].to_numpy()
dH_Kr = np.array([df_NAME["Xe_heat"],df_NAME["Kr_heat"]]).T
dH_Xe = np.array([df_NAME["Xe_heat"],df_NAME["Kr_heat"]]).T

print(Name_list)
print('Total Number of Candidate:')
print(len(Name_list))

Arrh = lambda T,dH ,T_ref: np.exp(-dH/8.3145*(1/T - 1/T_ref)) # Arrhenius equation (Clasius-Clapeyron Equation)

## Isothermal mixture isotherm
def iso_mix(P_par, T, iso_list, dH_list,Tref_list):
    P_norm = []
    for (p,dh,tref) in zip(P_par, dH_list,Tref_list):
        p_n = Arrh(T,dh,tref)*p 
        P_norm.append(p_n)
    P_norm_arr = np.array(P_norm)
    #print(P_norm_mat.T)
    if P_norm_arr.ndim > 1:
        for i in range(len(P_norm[0])):
            p_tmp = P_norm_arr[i,:]
            p_tmp[p_tmp<0.000001] = 0.000001
            q_IAST_tmp = pyiast.iast(p_tmp,
                                     iso_list,
                                     warningoff=True)
    else:
        try:
            p_tmp = P_norm_arr
            p_tmp[p_tmp<0.000001] = 0.000001
            #print(p_tmp)
            q_IAST_tmp = pyiast.iast(p_tmp,
                                    iso_list,
                                     warningoff=True)
        except:    
            try:
                #print('Initial guess error with P = ',P_par)
                x_IG = np.ones(len(p_tmp))/len(p_tmp)
                q_IAST_tmp = pyiast.iast(p_tmp,
                                        iso_list,adsorbed_mole_fraction_guess = x_IG,
                                        warningoff=True)
            except:
                try:
                    arg_min = np.argmin(p_tmp)
                    p_tmp[p_tmp<0.000001] = 0.000001
                    x_IG = 0.05*np.ones(len(p_tmp))
                    x_IG[arg_min] = 1 - 0.05*(len(p_tmp)-1)
                    #print(x_IG)
                    q_IAST_tmp = pyiast.iast(p_tmp,
                                            iso_list,adsorbed_mole_fraction_guess = x_IG,
                                            warningoff=True)

                except:
                    try:
                        arg_max = np.argmax(p_tmp)
                        p_tmp[p_tmp<0.000001] = 0.000001
                        x_IG = 0.05*np.ones(len(p_tmp))
                        x_IG[arg_max] = 1 - 0.05*(len(p_tmp)-1)
                        #print(x_IG)
                        q_IAST_tmp = pyiast.iast(p_tmp,
                                                iso_list,adsorbed_mole_fraction_guess = x_IG,
                                                warningoff=True)        
                    except:
                        try:
                            arg_max = np.argmax(p_tmp)
                            p_tmp[p_tmp<0.000001] = 0.000001
                            x_IG = 0.15*np.ones(len(p_tmp))
                            x_IG[arg_max] = 1 - 0.15*(len(p_tmp)-1)
                            #print(x_IG)
                            q_IAST_tmp = pyiast.iast(p_tmp,
                                                iso_list,adsorbed_mole_fraction_guess = x_IG,
                                                warningoff=True)
                        except:
                            try:
                                arg_min = np.argmin(p_tmp)
                                p_tmp[p_tmp<0.000001] = 0.000001
                                x_IG = 0.01*np.ones(len(p_tmp))
                                x_IG[arg_min] = 1 - 0.01*(len(p_tmp)-1)
                                #print(x_IG)
                                q_IAST_tmp = pyiast.iast(p_tmp,
                                            iso_list,adsorbed_mole_fraction_guess = x_IG,
                                            warningoff=True)

                            except:
                                arg_max = np.argmax(p_tmp)
                                p_tmp[p_tmp<0.000001] = 0.000001
                                x_IG = 0.01*np.ones(len(p_tmp))
                                x_IG[arg_max] = 1 - 0.01*(len(p_tmp)-1)
                                #print(x_IG)
                                q_IAST_tmp = pyiast.iast(p_tmp,
                                                iso_list,adsorbed_mole_fraction_guess = x_IG,
                                            warningoff=True)                                
           
    return q_IAST_tmp

def x2x(x_ini,P_high,P_low,
        iso_input, dH_input, Tref_input, 
        yfeed,Tfeed):
    iso_1 = iso_input[0] # Xe
    iso_2 = iso_input[1] # Kr
    iso  = [iso_1,iso_2]
    dH_1, dH_2 = dH_input[:2]         # (kJ/mol): Heat of adsorption
    dH = np.array([dH_1,dH_2])*1000    # (J/mol): Heat of adsorption 
    P_low_part = np.array(x_ini)*P_low      # (bar): partial pressure
    P_high_part = np.array(yfeed)*P_high    # (bar): partial pressure
    ### Uptakes
    #print(P_low_part)
    P_low_part = np.reshape(P_low_part,len(iso))
    q_des = iso_mix(P_low_part,Tfeed,iso,
                    dH,Tref_input)
    #print(P_high_part)
    P_high_part = np.reshape(P_high_part,len(iso))
    q_sat_tot = iso_mix(P_high_part,Tfeed,iso,
                        dH,Tref_input)
    Dq_tot = q_sat_tot-q_des
    ### Leading component ?
    sat_extent = np.array(yfeed)/Dq_tot # Saturation extent kg/mol
    ind_lead_tot = np.argmax(sat_extent)
    dq = q_sat_tot - q_des
    x_out = dq/(np.sum(dq))
    return x_out,ind_lead_tot

def rec(x_ini,P_high,P_low,
        iso_input, dH_input, Tref_input, 
        yfeed,Tfeed):
    def x_err(xx):
        x_new,i_lead = x2x([xx, 1-xx],P_high,P_low,
                           iso_input, dH_input, Tref_input, 
                           yfeed,Tfeed)
        return (xx-x_new[0])**2
    #sol = optim.minimize(x_err,x_ini,method='COBYLA')
    sol = optim.least_squares(x_err,x_ini,bounds = [0,1])
    x_sol = sol.x
    _,i_lead = x2x([x_sol, 1- x_sol],P_high,P_low,
                   iso_input, dH_input, Tref_input, 
                   yfeed,Tfeed)
    #if i_lead  < 0.5:
    #    return -1
    Recovery = 1-(1-x_sol)/x_sol*yfeed[0]/yfeed[1]
    if Recovery < 0 or Recovery > 1:
        Recovery = 1-x_sol/(1-x_sol)*yfeed[1]/yfeed[0]
 #   return Recovery, i_lead, x_sol+
    return Recovery, i_lead, x_sol

T_feed_in = 313         # (K) temperature or 298K
T_tri = [298.15,]*2
#y_feed_in = np.array([0.83356,0.1644])
y_ethy = 8/10
#y_ethy = 0.83356
y_feed_in = np.array([1-y_ethy,y_ethy])
Rec_list_set = []
xx_list_set = []
leading_index_set = []
#Pl_list = np.linspace(0.004,0.5,30)
Pl_list = 1/(10**np.linspace(0.5,3,101))

for binn,dH,nam in zip(bins_Kr,dH_Kr,Name_list):
    Rec_list = []
    x_list = []
    leading_index = []
    
    for pl in Pl_list:
        try:
            x_guess = 0.05
            rec_tmp,l_ind,x_tmp = rec(x_guess, 1,pl,
                                      binn, dH, T_tri,y_feed_in, T_feed_in)
        except:
            try:
                x_guess = 0.4
                rec_tmp,l_ind,x_tmp = rec(x_guess, 1,pl,
                                          binn, dH, T_tri,y_feed_in, T_feed_in)
            except:
                try:
                    x_guess = 0.8
                    rec_tmp,l_ind,x_tmp = rec(x_guess, 1,pl,
                                              binn, dH, T_tri,y_feed_in, T_feed_in)                        
                except:
                    try:
                        x_guess = 0.9
                        rec_tmp,l_ind,x_tmp = rec(x_guess, 1,pl,
                                                  binn, dH, T_tri,y_feed_in, T_feed_in)                        
                    except:
                        try:
                            x_guess = 0.95
                            rec_tmp,l_ind,x_tmp = rec(x_guess, 1,pl,
                                                      binn, dH, T_tri,y_feed_in, T_feed_in)                        
                        except:
                            x_guess = 0.98
                            rec_tmp,l_ind,x_tmp = rec(x_guess, 1,pl,
                                                      binn, dH, T_tri,y_feed_in, T_feed_in)
                        
        #x_guess[0] = x_tmp*1.01
        Rec_list.append(rec_tmp)
        x_list.append(x_tmp[0])
        leading_index.append(l_ind)
    Rec_list_set.append(Rec_list)
    xx_list_set.append(x_list)
    leading_index_set.append(leading_index)
    print(x_tmp)

Rec_sort_tmp = []
for i in range(len(Rec_list_set)):
    rec_tmm = np.reshape(np.array(Rec_list_set[i]),[-1])
    Rec_sort_tmp.append(rec_tmm)
Rec_sort_tmp = np.array(Rec_sort_tmp)

Sort_target = np.reshape(np.array(Rec_sort_tmp)[:,-1],-1)
#print(Sort_target)
arg_st = np.argsort(Sort_target)[::-1]
Name_sort = np.array(Name_list)[arg_st]

Rec_sort = Rec_sort_tmp[arg_st,:]
leading_sort = np.array(leading_index_set)[arg_st]
#is_exp_sort = is_exp[arg_st]

print(Pl_list[-5]*100)
print(Name_sort)
print(Rec_sort[:,-5])

for i in range(1242):
    print(Name_sort[i],Rec_sort[i][100])
