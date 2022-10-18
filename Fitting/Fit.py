# Import library.

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import math
import seaborn as sns

# define Langmuir equation.

def langmuir(p,M,K):
    return M*K*p/(1+K*p)

# Fit Langmuir parameters

for ZN in data["Filename"]:
    ZNN=str(ZN)
    data=pd.read_csv('./Concat/'+ZNN+'_Kr.csv')

    x = data["p"]
    y = data["q"]
    
    try:
        popt, pcov = curve_fit(langmuir, x, y,maxfev = 60000)

        M = popt[0] 
        K = popt[1]

        y_pre = langmuir(x,M,K) 
        correlation = np.corrcoef(y, y_pre)[0,1]

        print(ZNN,popt,correlation**2)
    except:
        print(ZNN,"Fail fit")

# Make figures

plt.rcParams.update({'figure.max_open_warning': 0})

p=np.linspace(0.00001,30,100)

for i,name in enumerate(data.Filename):
    fig = plt.figure(facecolor='w')
    
    data_gcmc_Xe=pd.read_csv('./Concat/'+name+'_Xe.csv')
    data_gcmc_Kr=pd.read_csv('./Concat/'+name+'_Kr.csv')
    
    qXe1=langmuir(p,data.Xe_M[i],data.Xe_K[i])
    
    qKr1=langmuir(p,data.Kr_M[i],data.Kr_K[i])
    
    plt.plot(p, qXe1, '-.', color='black', linewidth=3,label='Fit_Langmuir_Xe',zorder=0)
    plt.scatter(data_gcmc_Xe.p, data_gcmc_Xe.q, color='blue',edgecolor='k', label='GCMC_Xe',zorder=1,s=100)

    plt.plot(p, qKr1, '-.', color='black', linewidth=3,label='Fit_Langmuir_Kr',zorder=0)
    plt.scatter(data_gcmc_Kr.p, data_gcmc_Kr.q, color='red',edgecolor='k', label='GCMC_Kr',zorder=1,s=100)
    
    plt.xlabel("Pressure (bar)",fontdict={'family':'Calibri','size':20})
    plt.title(name)
    
    Xe_M="Xe-M:"+str(format(data.Xe_M[i],'.2E'))
    Xe_K="Xe-K:"+str(format(data.Xe_K[i],'.2E'))
    Kr_M="Kr-M:"+str(format(data.Kr_M[i],'.2E'))
    Kr_K="Kr-K:"+str(format(data.Kr_K[i],'.2E'))
    
    loc=max(data_gcmc_Xe.q)
    
    plt.text(0.0001,loc,Xe_M)
    plt.text(0.0001,loc*0.2,Xe_K)
    plt.text(0.0001,loc*0.02,Kr_M)
    plt.text(0.0001,loc*0.002,Kr_K)
    
#     ylim2=float(max(max(qXe1),max(qXe2)))*1.1
#     ylim1=float(min(min(qKr1),min(qKr2)))*0.9
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim([0.000009, 30])    
#     plt.ylim([ylim1, ylim2]) 
    
#     plt.xticks([ ])
#     plt.yticks([ ])
#     plt.legend(prop={'family':'Calibri','size':10},frameon=False)
    plt.ylabel("Uptake (mmol/g)",fontdict={'family':'Calibri','size':20})
    
    plt.savefig('./Fig_Fit/'+name+'.png',dpi=100, bbox_inches='tight')
    
    plt.show()
