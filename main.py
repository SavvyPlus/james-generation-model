import pandas as pd
from solar_angle_calculations import calculate_angle
from radiation_calculation import calculate_radiation
from util import *


if __name__ == '__main__':

    IO = 'Solar PV Model Rev1.6.xlsx'
    df = pd.read_excel(io=IO, sheet_name='Data Dump', usecols="A:C", parse_dates=['TimeStamp'])
    df_org = pd.read_excel(IO, sheet_name='Model Calcs', usecols="A:Z", parse_dates=['Date']).dropna()
    df = calculate_angle(df)
    result = sum( list(a - b for a,b in zip(df[col_solar_azimuth_ang], df_org[col_solar_azimuth_ang])))
    print(result)
    df = calculate_radiation(df)
    df_org = pd.read_excel(IO, sheet_name='Model Calcs', usecols="AB:AD").dropna()
    result = sum( list(a - b for a,b in zip(df[col_dhi], df_org[col_dhi])))
    print(result)