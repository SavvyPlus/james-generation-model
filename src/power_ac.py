import pandas as pd

from util import col_ac_w, col_ac_kw, col_ac_kw_invert_losses, col_dc_array

"""
Description:

This is a function used to compute AC power from an inverter for a given solar panel. 

Inputs:

Calculated DC Power obtained from solar panel in Watts
Inverter Size in kW
Inverter Efficiency in % 

Outputs:

AC Power in Watts
AC Power in kW
AC Power including losses in kW

"""


def power_ac_calculation(df: pd.DataFrame, invertsize: float,
                         invertefficiency: float) -> pd.DataFrame:
    df[col_ac_w] = df[col_dc_array].map(lambda x: min(x, invertsize * 1000))
    df[col_ac_kw] = df[col_ac_w].map(lambda x: x / 1000)
    df[col_ac_kw_invert_losses] = df[col_ac_kw].map(lambda x: x * invertefficiency)
    return df
