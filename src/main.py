import DTiH_data_loader as dtdl
import DTiH_score_system as dtss
import DTiH_annalyzing_ppg as dtppg

import pandas as pd


from DTiH_data_loader import Activity
from enum import Enum

class Predictor(Enum):
    LIFESTYLE = 'lifestyle'
    PPG = 'ppg'

class Hazardratio(Enum):
    RMSSD = {'name': 'rmssd',       	'hazardratio':1.036, 'predictor': Predictor.PPG}
    PNN50 = {'name': 'pnn50',           'hazardratio':1.057, 'predictor': Predictor.PPG}
    LFHF  = {'name': 'lf/hf',           'hazardratio':0.509, 'predictor': Predictor.PPG}
    
    BMI   = {'name': 'BMI',             'hazardratio':1.036, 'predictor': Predictor.LIFESTYLE}
    SMOKING = {'name':'smoking',        'hazardratio':0.55 , 'predictor': Predictor.LIFESTYLE}


SAMPLE_RATE = 400

def procces_all(predictors: list) -> pd.DataFrame:

    df_risk = pd.DataFrame(columns=['patient'] + [hz.value['name'] for hz in predictors])

    df_ppg = dtdl.load_all_mat_by_activity(Activity.resting)
    for name, values in df_ppg.iteritems():
        values.dropna(inplace = True)
        preprocessed_data = dtppg.preprocessing_ppg_signal(values.tolist(),SAMPLE_RATE)
        _, mesurement = dtppg.peak_detection(preprocessed_data,SAMPLE_RATE)

        df_risk = df_risk.append({'patient': values.name,'rmssd':  mesurement['rmssd'], 'pnn50': mesurement['pnn50'], 'lf/hf': mesurement['lf/hf']}, ignore_index=True)

    df_risk.fillna(0, inplace=True)

    return df_risk
  
if __name__ == '__main__':
    df_input = procces_all([hz for hz in Hazardratio])
    df_input = dtppg.counting_score3(df_input)
    print(dtss.calculate_score(df_input))
