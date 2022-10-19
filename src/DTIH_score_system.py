# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 11:22:25 2022

@author: 20212238
"""

import pandas as pd

#format for patient data: [BMI,ADS,CDS,RMSSD,pNN50,LF/HF]

patient_data = [[28,23,12,1,1,1],[25,2,30,1,0,1],[32,12,23,0,1,1]]

def category(factor,v1,v2,v3,v4,s0 = 0,s1 = 1,s2 = 2,s3 = 3,s4 = 4):
    if factor < v1:
        score = s0
    elif factor < v2:
        score = s1
    elif factor < v3:
        score = s2
    elif factor < v4:
        score = s3
    elif factor >= v4:
        score = s4
    return score
        
#print(category(25,18.5,25,30,35,1,0))

def total_score(patient_data_list):
    for i in range(len(patient_data_list)):
        
        BMI_score = category(patient_data_list[i][0],18.5,25,30,35,1,0)*1.03
        ADS_score = category(patient_data_list[i][1],1,14,22,31)*1.23
        CDS_score = category(patient_data_list[i][2],1,14,22,31)*0.55
        
        RMSSD_score = patient_data_list[i][3]*1.036
        pNN50_score = patient_data_list[i][4]*1.057
        LF_HF_score = patient_data_list[i][5]*0.509
        
        PPG_score = (RMSSD_score + pNN50_score + LF_HF_score)*0.75/2.602
        lifestyle_score = (BMI_score + ADS_score + CDS_score)*0.25/11.24
        
        if PPG_score == 0.75:
            risk_score = 1
        else:
            risk_score = PPG_score + lifestyle_score
        
        print('Patient',i+1,'\nBMI-score:',BMI_score,'\nADS-score:',ADS_score,'\nCDS-score:',CDS_score,'\nRMSSD-score:',RMSSD_score,'\npNN50-score:',pNN50_score,'\nLF/HF-score:',LF_HF_score,'\nlifestyle-score:',lifestyle_score,'\nPPG-score:',PPG_score,'\nRisk-score:',risk_score)
        print(' ')

def calculate_score(df_input: pd.DataFrame) -> pd.DataFrame:
    df_input["ppg_predictors"] = (1.036* df_input['normalized_rmssd'] + 1.057 * df_input['normalized_pnn50'] + 0.509 * df_input['normalized_lf/hf']) / 2.602
    df_input['lifestyle_predictors'] = (1.03 * df_input['BMI'] + 1.23 * df_input['smoking'])
    df_input['chance'] = (0.75 * df_input['ppg_predictors'] + 0.25 * df_input['lifestyle_predictors']) /0.75
    return df_input


if __name__ == '__main__': 
    total_score(patient_data)   
        