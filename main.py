import pandas as pd
from solar_angle_calculations import calculate_angle
from util import *


if __name__ == '__main__':

    IO = 'Solar PV Model Rev1.6.xlsx'
    df = pd.read_excel(io=IO, sheet_name='Data Dump', usecols="A:C", parse_dates=['TimeStamp'])
    df_org = pd.read_excel(IO, sheet_name='Model Calcs', usecols="A:Z", parse_dates=['Date']).dropna()
    df = calculate_angle(df)
    result = (df[col_solar_azimuth_ang] - df[col_solar_azimuth_ang]).sum()
    print(result)