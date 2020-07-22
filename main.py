import pandas as pd
from solar_angle_calculations import calculate_angle
from radiation_calculation import calculate_radiation
from util import *


if __name__ == '__main__':

    IO = 'Solar PV Model Rev1.6.xlsx'
    df = pd.read_excel(io=IO, sheet_name='Data Dump', usecols="A:C", parse_dates=['TimeStamp'])
    df_org = pd.read_excel(IO, sheet_name='Model Calcs', usecols="AB:AD").dropna()
    df = calculate_angle(df)

    df = calculate_radiation(df)
    result = (df[col_dhi] - df[col_dhi]).sum()
    print(result)