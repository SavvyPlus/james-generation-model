import math
import pandas as pd

from util import col_perez_a, col_perez_b, col_perez_sky, col_aoi_deg, col_solar_zen_ang, \
    col_perez_sky, col_dni, col_ghi, col_dhi, col_perez_air_mass_optical, col_perez_delta, \
    col_perez_f11, col_perez_f12, col_perez_f13, col_perez_f21, col_perez_f22, col_perez_f23, \
    col_perez_F1, col_perez_F2, col_model, col_Di, col_Dc, col_Dh

# Look up table for f11,f12,f13,f21.f22 and f23 calculations
Look_Up = [[-0.008312, 0.587728, -0.06206, -0.59601, 0.072125, -0.022022],
           [0.129946, 0.682595, -0.151375, -0.018933, 0.065965, -0.028875],
           [0.329696, 0.486874, -0.221096, 0.055414, -0.063959, -0.026054],
           [0.568205, 0.187452, -0.295129, 0.108863, -0.151923, -0.013975],
           [0.873028, -0.392040, -0.361615, 0.225565, -0.462044, 0.001245],
           [1.132608, -1.236728, -0.411849, 0.287781, -0.823036, 0.055865],
           [1.060159, -1.599914, -0.358922, 0.264212, -1.27234, 0.131069],
           [0.677747, -0.327259, -0.250429, 0.156131, -1.376503, 0.250621]]

"""
Description:

A function to generate Perez model parameters for a solar panel

Inputs:

Angle of incidence in degrees
Solar Zenith angle in degrees
Diffused Normal Irradiance in W/m^2
Diffuse Horizontal Irradiance in W/m^2
Angle of tilt in degrees

Outputs:

Perez parameters including

Perez a, b, sky clearness,Air Mass Optical, delta, f11, f12, f13, f21, f22, f23, F1, F2.
Model used for calculations (Perez or Isotropic)
Isotropic Diffuse (Di) in W/m^2
Horizontal Diffuse (Dh) in W/m^2
Diffuse Irradiance (Dc) in W/m^2

"""


def get_perez_a(aoi_d: float):
    return max(0.0, math.cos(math.radians(aoi_d)))


def get_perez_b(zenith: float):
    return max(math.cos(math.radians(85)), math.cos(math.radians(zenith)))


def get_perez_air_mass(zenith: float, perez_b: float):
    if zenith <= 93.5:
        perez_air_mass = (math.cos(math.radians(perez_b)) + (
                0.15 * (93.15 - zenith)) ** -1.253) ** -1
    else:
        perez_air_mass = 1

    return perez_air_mass


def get_perez_delta(dhi: float, perez_air_mass_optical: float):
    return (dhi * perez_air_mass_optical) / 1367

def get_perez_param(perez_sky:float,perez_delta:float,zenith:float):
     
     i = int(perez_sky > 1.065) + int(perez_sky > 1.23) + int(perez_sky > 1.5) + int(perez_sky > 1.95) \
            + int(perez_sky > 2.8) + int(perez_sky > 4.5) + int(6.2 < perez_sky <= 100000)
    
     perez_f11, perez_f12, perez_f13, perez_f21, perez_f22, perez_f23 = [Look_Up[i][j] for j in range(6)]
     
     perez_F1 = max(0.0, perez_f11 + (perez_delta * perez_f12) + (math.radians(zenith) * perez_f13))
    
     perez_F2 = perez_f21 + (perez_delta * perez_f22) + (math.radians(zenith) * perez_f23)
     
     return perez_f11, perez_f12, perez_f13, perez_f21, perez_f22, perez_f23,perez_F1,perez_F2

def get_diffuse_values(dhi:float, tiltangle:float,zenith:float,perez_F1 :float,perez_F2 :float):
    
    if 87.5 <= zenith <= 90.0:
        model = 'Isotropic'
        Di = 0.5 * dhi * (1 + math.cos(math.radians(tiltangle)))
        Dc = 0.0
        Dh = 0.0
    
    else:
        model = 'Perez'
        Di = 0.5 * dhi * (1 - perez_F1) * (1 + math.cos(math.radians(tiltangle)))
        Dc = dhi * perez_F1 * perez_a / perez_b
        Dh = dhi * perez_F2 * math.sin(math.radians(tiltangle))
        
        return model, Di, Dc, Dh


def perez(df: pd.DataFrame, tiltangle: float):
    
    df[col_perez_a] = df[col_aoi_deg].map(get_perez_a)
    
    df[col_perez_b] = df[col_solar_zen_ang].map(get_perez_b)
    
    df[col_perez_sky] = df.apply(lambda x: (x[col_dni] + x[col_dhi]) / (
            (x[col_dhi] + 5.534e-6) * x[col_solar_zen_ang] ** 3 * (
            1 + (5.534e-6 * x[col_solar_zen_ang] ** 3))), axis=1)
    
    df[col_perez_air_mass_optical] = df.apply(
        lambda x: get_perez_air_mass(x[col_solar_zen_ang], x[col_perez_b]), axis=1)
    
    df[col_perez_delta] = df.apply(
        lambda x: get_perez_delta(x[col_dhi], x[col_perez_air_mass_optical]),axis=1)
    
    df[col_perez_f11],df[col_perez_f12],df[col_perez_f13],df[col_perez_f21],
    df[col_perez_f22], df[col_perez_f23],df[col_perez_F1],df[col_perez_F2] = df.apply(
        lambda x: get_perez_param(x[col_perez_sky],x[col_perez_delta],x[col_solar_zen_ang]),axis=1)
     
    df[col_model],df[col_Di], df[col_Dc], df[col_Dh]= df.apply(
        lambda x: get_diffuse_values(x[col_dhi],tiltangle,x[col_solar_zen_angle],x[col_perez_F1],x[col_perez_F2]), axis=1)
     
    return df
