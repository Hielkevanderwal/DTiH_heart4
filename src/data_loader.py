from scipy.io import loadmat
from enum import Enum

import pandas as pd


class Activity(Enum):
    resting = "rest"
    squatting = "squat"
    walking = "step"

subjects = {
    1 : {"height": 1.73, "Weight": 70, "BMI": 23.4, "AGE": 22, "Sex": "M"},
    2 : {"height": 1.78, "Weight": 72, "BMI": 22.7, "AGE": 22, "Sex": "M"},
    3 : {"height": 1.80, "Weight": 80, "BMI": 24.7, "AGE": 44, "Sex": "M"},
    4 : {"height": 1.70, "Weight": 60, "BMI": 20.8, "AGE": 52, "Sex": "F"},
    5 : {"height": 1.65, "Weight": 55, "BMI": 20.2, "AGE": 20, "Sex": "F"},
    6 : {"height": 1.57, "Weight": 66, "BMI": 26.8, "AGE": 41, "Sex": "F"},
    7 : {"height": 1.78, "Weight": 83, "BMI": 26.2, "AGE": 20, "Sex": "F"},
}
    

DATA_FOLDER_PATH = "C:\\Users\\20212498\\Documents\\studeren\\jaar 2\\8LEU01 Digital Twin in Healthcare 1\\Github\\data\\1-s2.0-S2352340919314003-mmc1"


def load_mat(activity: Activity, subject: int, sample: int, With_acc: bool = False) -> pd.DataFrame:
    """
    Load a specific mat file by choosing the activity and N (0 < N <= 5) And return a Dataframe containing the data of the .mat.
    """
    loaded_mat = loadmat("{}\\PPG_ACC_dataset\\S{}\\{}{}_ppg.mat".format(
        DATA_FOLDER_PATH,
        subject,
        activity.value,
        sample
    ))
    return pd.DataFrame(loaded_mat["PPG"], columns=["time","ppg_{}_S{}_N{}".format(
        activity.value,
        subject,
        sample
    )])

def load_all_mat_by_activity(activity: Activity) -> pd.DataFrame:
    return_df = pd.DataFrame()
    for subject in subjects:
        for sample in range(1,6):
            try:
                temp_df = load_mat(activity, subject, sample)
                temp_df.set_index("time", inplace=True)
                return_df = pd.concat([return_df, temp_df], axis="columns")
            except:
                print("skipping S{}N{}, because reading failled!".format(
                    subject, sample, 
                ))

    return return_df

if __name__ == '__main__':
    df = load_all_mat_by_activity(Activity.resting)
    print(df)