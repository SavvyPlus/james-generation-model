import pandas as pd
from solar_angle_calculations import calculate_angle
from radiation_calculation import calculate_radiation
from aoi_calculation import aoi_calculation
from perez_model import perez
from util import *

orientation = 0
tiltangle = 28



if __name__ == '__main__':
    IO = '../Solar PV Model Rev1.6.xlsx'
    df = pd.read_excel(io=IO, sheet_name='Data Dump', usecols="A:C", parse_dates=['TimeStamp'])
    # df_org = pd.read_excel(IO, sheet_name='Model Calcs', usecols="A:Z", parse_dates=['Date']).dropna()

    # calculate solar angle
    df = calculate_angle(df)

    # result = sum( list(a - b for a,b in zip(df[col_solar_azimuth_ang], df_org[col_solar_azimuth_ang])))
    # print(result)

    # normalize solar radiation data
    df = calculate_radiation(df)
    # df_org = pd.read_excel(IO, sheet_name='Model Calcs', usecols="AB:AD").dropna()
    # result = sum( list(a - b for a,b in zip(df[col_dhi], df_org[col_dhi])))
    # print(result)

    # calculate angle of incidence (AOI)
    df = aoi_calculation(df, orientation, tiltangle)

    # run perez model
    df = perez(df, tiltangle)