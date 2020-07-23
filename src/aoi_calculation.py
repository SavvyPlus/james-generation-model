import math
import pandas as pd
from util import col_aoi_rad, col_aoi_deg, col_solar_zen_ang, col_solar_azimuth_ang

"""
Description:

Function to obtain Angle of incidence for a given solar panel

Inputs:

Angle of orientation in degrees of the panel 
Angle of tilt in degrees of the panel 
Solar zenith angle in degrees of the given panel location 
Solar azimuth angle in degrees of the given panel location 

Outputs:

Angle of incidence of the solar panel in degrees and radians

"""


def get_rad(orient: float, zenith: float, azimuth: float, tiltangle: float):
    return math.sin(math.radians(zenith)) * math.cos(
        math.radians(azimuth - orient)) * math.sin(math.radians(tiltangle)) \
           + math.cos(math.radians(zenith)) * math.cos(math.radians(tiltangle))


def get_deg(rad: float):
    return math.degrees(math.acos(rad))


def aoi_calculation(df: pd.DataFrame, orient: float, tiltangle: float):
    df[col_aoi_rad] = df.apply(
        lambda x: get_rad(orient, x[col_solar_zen_ang], x[col_solar_azimuth_ang],
                          tiltangle), axis=1)
    df[col_aoi_deg] = df[col_aoi_rad].map(get_deg)
    return df

# AOI_rad,AOI_deg=AOI(0,28,116.122,201.302)
# print(AOI_rad)
# print(AOI_deg)
