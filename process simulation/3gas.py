import pandas as pd
import numpy as np
from tqdm import tqdm
import pyiast
import scipy.optimize as optim
import os
import matplotlib.pyplot as plt
import pickle
import csv
from scipy.optimize import curve_fit

def iso_mix(P_par, T, M_list, h_list, dH_list):
    p = np.linspace(0, 100, 100)
    q_1 = np.zeros(100)
    q_2 = np.zeros(100)
    q_3 = np.zeros(100)
    
    for i in range(100):
        M1, M2, M3, = M_list
        K1=h_list[0] * 100000 / M1
        K2=h_list[1] * 100000 / M2
        K3=h_list[2] * 100000 / M3
        
        Q1[i] = langmuir(p[i],M1,K1)
        Q2[i] = langmuir(p[i],M2,K2)
        Q3[i] = langmuir(p[i],M3,K3) 
        
    df_ISO_list = [
        pd.DataFrame({'p': p, 'q': Q1}),
        pd.DataFrame({'p': p, 'q': Q2}),
        pd.DataFrame({'p': p, 'q': Q3})
    ]
    
    iso_list = [
        pyiast.ModelIsotherm(df_ISO_list[0], loading_key='q', pressure_key='p', model='Langmuir', param_guess={"M": M1, "K": K1}),
        pyiast.ModelIsotherm(df_ISO_list[1], loading_key='q', pressure_key='p', model='Langmuir', param_guess={"M":  M2, "K": K2}),
        pyiast.ModelIsotherm(df_ISO_list[2], loading_key='q', pressure_key='p', model='Langmuir', param_guess={"M":  M3, "K": K3})
    ]
    
    P_norm = [Arrh(T, dh, T) * pp for pp, dh in zip(P_par, dH_list)]
    P_norm_arr = np.array(P_norm)
    q_IAST_tmp = pyiast.iast(P_norm_arr.T, iso_list, warningoff=True)
    S = q_IAST_tmp[0] / q_IAST_tmp[1]
    return q_IAST_tmp, S


def x2x(x_ini, P_high, P_low, M_list, h_list, dH_input, yfeed, Tfeed):
    dH = np.array(dH_input) * 1000
    P_low_part = np.array(x_ini) * P_low
    P_high_part = np.array(yfeed) * P_high
    
    q_des = iso_mix(P_low_part, Tfeed, M_list, h_list, dH)[0]
    q_sat_tot = iso_mix(P_high_part, Tfeed, M_list, h_list, dH)[0]
    
    dq = q_sat_tot - q_des
    x_out = dq / np.sum(dq)
    ind_lead_tot = np.argmax(dq / yfeed) 
    return x_out, ind_lead_tot

def rec(x_ini, P_high, P_low, M_list, h_list, dH_input, yfeed, Tfeed):
    def x_err(x):
        x_new, i_lead = x2x(x, P_high, P_low, M_list, h_list, dH_input, yfeed, Tfeed)
        return np.sum((x - x_new) ** 2)
    
    sol = optim.least_squares(x_err, x_ini, bounds=(0, 1))
    if sol.success:
        x_sol = sol.x
        Recovery, i_lead = x2x(x_sol, P_high, P_low, M_list, h_list, dH_input, yfeed, Tfeed)
        return Recovery, i_lead, x_sol
    else:
        print(f"Optimization failed for {Name_list_all}: {sol.message}")
        return None, None, None

T_feed_in = 298 
T_tri = [298, 298]

y1 = 0.2 
y2 = 0.2
y3 = 0.6

p = 0.1
df = pd.read_excel("data.xlsx", sheet_name = "all")


Name_list_all = df["Filename"]
M_list_all = df[["M1", "M2", "M3"]]
h_list_all = df[["henry1", "henry2", "henry3"]]
H_list_all = df[["heat1", "heat2", "heat3"]]

y_feed_in = np.array([y1, y2, y3])
Rec_list_set = []
xx_list_set = []
leading_index_set = []

p = 0.1

x_guesses = [0.05, 0.4, 0.8, 0.9, 0.95, 0.98]

for M_list, h_list, dH, nam in zip(M_list_all.values, h_list_all.values, H_list_all.values, Name_list_all):
    Rec_list = []
    x_list = []
    leading_index = []
    rec_tmp, l_ind, x_tmp = None, None, None  # 初始化变量
    
    # 循环尝试不同的x_guess直到一个成功或所有尝试都失败
    for x_guess in x_guesses:
        try:
            rec_tmp, l_ind, x_tmp = rec(x_guess, 1, p, M_list, h_list, dH, y_feed_in, T_feed_in)
            break  # 如果成功获取结果，跳出循环
        except Exception as e:
            print(f"Failed for {nam} at x_guess={x_guess} with error: {e}")
    
    if rec_tmp is not None:
        print(f"{nam}: Recovery={rec_tmp}, Leading Index={l_ind}, x={x_tmp}")
    else:
        print(f"Failed to process {nam} with any x_guess")
