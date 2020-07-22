
import pandas as pd
from solar_angle_calculations import *
from util import *


def DNI_on_Horizontal(dni):
    return dni if dni > 0 else 0


def DHI_on_horizontal(dni, ghi, solar_zen_ang):
    dhi = ghi - (dni * math.cos(math.radians(solar_zen_ang)))
    return dhi if dhi >= 0 else 0


def calculate_radiation(df: pd.DataFrame) -> pd.DataFrame:
    """calculate radiation DNI, GHI and DHI from original raw data
    :param df: data frame with DNI and GHI column
    """
    df[col_dni] = df['DNI'].map(DNI_on_Horizontal)
    df[col_ghi] = df['GHI']
    df[col_dhi] = df.apply(lambda x: DHI_on_horizontal(x[col_dni],
                                                       x[col_ghi],
                                                       x[col_solar_zen_ang]), axis=1)

    return df
