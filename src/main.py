from data_loader import load_all_mat_by_activity, Activity
from DTIH_score_system import calculate_score

from enum import Enum

import annalyzing_ppg as appg

import pandas as pd

SAMPLE_RATE = 400

class Predictor(Enum):
    LIFESTYLE = 'lifestyle'
    PPG = 'ppg'

class Hazardratio(Enum):
    RMSSD = {'name': 'rmssd',       	'hazardratio':1.036, 'predictor': Predictor.PPG}
    PNN50 = {'name': 'pnn50',           'hazardratio':1.057, 'predictor': Predictor.PPG}
    LFHF  = {'name': 'lf/hf',           'hazardratio':0.509, 'predictor': Predictor.PPG}
    
    BMI   = {'name': 'BMI',             'hazardratio':1.036, 'predictor': Predictor.LIFESTYLE}
    SMOKING = {'name':'Smoking',        'hazardratio':0.55 , 'predictor': Predictor.LIFESTYLE}


def procces_all(predictors: list) -> pd.DataFrame:

    df_risk = pd.DataFrame(columns=['patient'] + [hz.value['name'] for hz in predictors])

    df_ppg = load_all_mat_by_activity(Activity.resting)
    for name, values in df_ppg.iteritems():
        values.dropna(inplace = True)
        preprocessed_data = appg.preprocessing_ppg_signal(values.tolist(),SAMPLE_RATE)
        _, mesurement = appg.peak_detection(preprocessed_data,SAMPLE_RATE)

        df_risk = df_risk.append({'patient': values.name,'rmssd':  mesurement['rmssd'], 'pnn50': mesurement['pnn50'], 'lf/hf': mesurement['lf/hf']}, ignore_index=True)

    df_risk.fillna(0, inplace=True)

    return df_risk
  
if __name__ == '__main__':
    df_input = procces_all([hz for hz in Hazardratio])
    print(calculate_score(df_input))