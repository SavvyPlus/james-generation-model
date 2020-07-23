import pandas as pd
from solar_angle_calculations import calculate_angle
from radiation_calculation import calculate_radiation
from aoi_calculation import aoi_calculation
from perez_model import perez
from poa_calc import effective_poa_calculation
from power_dc import power_dc_calculation
from power_ac import power_ac_calculation
from util import *


orientation = 0
tiltangle = 28
lossfactortoggle = 1
pvefficiency = 0.19
panel_num = 18
area_per_panel = 1.5
invertsize = 5.3
invertefficiency = 0.96
sys_losses = {
    'soiling': 0.02,
    'shading': 0.03,
    'snow': 0.0,
    'mismatch': 0.02,
    'wiring': 0.02,
    'connections': 0.005,
    'lid': 0.015,
    'nameplate': 0.01,
    'age': 0.0,
    'availability': 0.02,
}

if __name__ == '__main__':
    IO = '../Solar PV Model Rev1.6.xlsx'
    df = pd.read_excel(io=IO, sheet_name='Data Dump', usecols="A:C",
                       parse_dates=['TimeStamp'])

    # calculate solar angle
    df = calculate_angle(df)

    # normalize solar radiation data
    df = calculate_radiation(df)

    # calculate angle of incidence (AOI)
    df = aoi_calculation(df, orientation, tiltangle)

    # run perez model
    df = perez(df, tiltangle)

    # calculate effective poa
    df = effective_poa_calculation(df, tiltangle)

    # calculate power DC
    df = power_dc_calculation(df, lossfactortoggle, pvefficiency, sys_losses, panel_num,
                              area_per_panel)

    # calculate final power AC
    df = power_ac_calculation(df, invertsize, invertefficiency)
    df.to_csv('final.csv')

    # comparison
    df_org = pd.read_excel(IO, sheet_name='Model Calcs', usecols="BH:BL").dropna()
    result = sum(list(a - b for a, b in zip(df[col_ac_kw_invert_losses], df_org['Power AC\nkW\ninc Inverter losses'])))
    print(result)