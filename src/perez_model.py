import math
import pandas as pd

from util import col_perez_a, col_perez_b, col_aoi_deg, col_solar_zen_ang, \
    col_perez_sky, col_dni, col_dhi, col_perez_air_mass_optical, col_perez_delta, \
    col_perez_f11, col_perez_f12, col_perez_f13, col_perez_f21, col_perez_f22, \
    col_perez_f23, col_perez_f1, col_perez_f2, col_model, col_di, col_dc, col_dh

# Look up table for f11,f12,f13,f21.f22 and f23 calculations
Look_Up = [[-0.0083117, 0.5877285, -0.0620636, -0.0596012, 0.0721249, -0.0220216],
           [0.1299457, 0.6825954, -0.1513752, -0.0189325, 0.065965, -0.0288748],
           [0.3296958, 0.4868735, -0.2210958, 0.055414, -0.0639588, -0.0260542],
           [0.5682053, 0.1874525, -0.295129, 0.1088631, -0.1519229, -0.0139754],
           [0.873028, -0.3920403, -0.3616149, 0.2255647, -0.4620442, 0.0012448],
           [1.1326077, -1.2367284, -0.4118494, 0.2877813, -0.8230357, 0.0558651],
           [1.0601591, -1.5999137, -0.3589221, 0.2642124, -1.127234, 0.1310694],
           [0.677747, -0.3272588, -0.2504286, 0.1561313, -1.3765031, 0.2506212]]

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


def get_perez_air_mass(zenith: float, perez_b: float) -> float:
    # if zenith == 93.15:
    #     perez_air_mass = 1.0
    # else:
    #     part = 0.15 * (93.15 - zenith)
    #     perez_air_mass = (math.cos(math.radians(perez_b)) +
    #                       abs(0.15 * (93.15 - zenith)) ** -1.253) ** -1

    perez_air_mass = (math.cos(math.radians(perez_b)) + (
            0.15 * (93.15 - zenith)) ** -1.253) ** -1

    if isinstance(perez_air_mass, complex):
        perez_air_mass = 1.0

    return perez_air_mass


def get_perez_delta(dhi: float, perez_air_mass_optical: float):
    return (dhi * perez_air_mass_optical) / 1367


def get_index(perez_sky: float):
    i = int(perez_sky > 1.065) + int(perez_sky > 1.23) + int(perez_sky > 1.5) + int(
        perez_sky > 1.95) \
        + int(perez_sky > 2.8) + int(perez_sky > 4.5) + int(6.2 < perez_sky <= 100000)
    return i


def get_perez_f11(perez_sky: float):
    i = get_index(perez_sky)
    return Look_Up[i][0]


def get_perez_f12(perez_sky: float):
    i = get_index(perez_sky)
    return Look_Up[i][1]


def get_perez_f13(perez_sky: float):
    i = get_index(perez_sky)
    return Look_Up[i][2]


def get_perez_f21(perez_sky: float):
    i = get_index(perez_sky)
    return Look_Up[i][3]


def get_perez_f22(perez_sky: float):
    i = get_index(perez_sky)
    return Look_Up[i][4]


def get_perez_f23(perez_sky: float):
    i = get_index(perez_sky)
    return Look_Up[i][5]


def get_perez_f1(perez_f11: float, perez_delta: float, perez_f12: float, zenith: float,
                 perez_f13: float) -> float:
    return max(0.0, perez_f11 + (perez_delta * perez_f12) +
               (math.radians(zenith) * perez_f13))


def get_perez_f2(perez_f21: float, perez_delta: float, perez_f22: float, zenith: float,
                 perez_f23: float) -> float:
    return perez_f21 + (perez_delta * perez_f22) + (math.radians(zenith) * perez_f23)


def get_model(zenith: float) -> str:
    if 87.5 < zenith < 90.0:
        return 'Isotropic'
    else:
        return 'Perez'


def get_di(model: str, dhi: float, tiltangle: float, perez_f1: float) -> float:
    if model == 'Isotropic':
        di = 0.5 * dhi * (1 + math.cos(math.radians(tiltangle)))
    else:
        di = 0.5 * dhi * (1 - perez_f1) * (1 + math.cos(math.radians(tiltangle)))

    return di


def get_dc(model: str, dhi: float, perez_f1: float, perez_a: float,
           perez_b: float) -> float:
    if model == 'Isotropic':
        dc = 0.0
    else:
        dc = dhi * perez_f1 * perez_a / perez_b

    return dc


def get_dh(model: str, dhi: float, perez_f2: float, tiltangle: float) -> float:
    if model == 'Isotropic':
        dh = 0.0
    else:
        dh = dhi * perez_f2 * math.sin(math.radians(tiltangle))

    return dh


def perez(df: pd.DataFrame, tiltangle: float):
    df[col_perez_a] = df[col_aoi_deg].map(get_perez_a)

    df[col_perez_b] = df[col_solar_zen_ang].map(get_perez_b)

    df[col_perez_sky] = df.apply(lambda x: (x[col_dni] + x[col_dhi]) / (
            (x[col_dhi] + 5.534e-6) * x[col_solar_zen_ang] ** 3 * (
            1 + (5.534e-6 * x[col_solar_zen_ang] ** 3))), axis=1)

    df[col_perez_air_mass_optical] = df.apply(
        lambda x: get_perez_air_mass(x[col_solar_zen_ang], x[col_perez_b]), axis=1)

    df[col_perez_delta] = df.apply(
        lambda x: get_perez_delta(x[col_dhi], x[col_perez_air_mass_optical]), axis=1)

    df[col_perez_f11] = df[col_perez_sky].map(get_perez_f11)
    df[col_perez_f12] = df[col_perez_sky].map(get_perez_f12)
    df[col_perez_f13] = df[col_perez_sky].map(get_perez_f13)
    df[col_perez_f21] = df[col_perez_sky].map(get_perez_f21)
    df[col_perez_f22] = df[col_perez_sky].map(get_perez_f22)
    df[col_perez_f23] = df[col_perez_sky].map(get_perez_f23)
    df[col_perez_f1] = df.apply(lambda x: get_perez_f1(x[col_perez_f11],
                                                       x[col_perez_delta],
                                                       x[col_perez_f12],
                                                       x[col_solar_zen_ang],
                                                       x[col_perez_f13]), axis=1)
    df[col_perez_f2] = df.apply(lambda x: get_perez_f2(x[col_perez_f21],
                                                       x[col_perez_delta],
                                                       x[col_perez_f22],
                                                       x[col_solar_zen_ang],
                                                       x[col_perez_f23]), axis=1)
    df[col_model] = df[col_solar_zen_ang].map(get_model)
    df[col_di] = df.apply(
        lambda x: get_di(x[col_model], x[col_dhi], tiltangle, x[col_perez_f1]))
    df[col_dc] = df.apply(
        lambda x: get_dc(x[col_model], x[col_dhi], x[col_perez_f1], x[col_perez_a],
                         x[col_perez_b]))
    df[col_dh] = df.apply(
        lambda x: get_dh(x[col_model], x[col_dhi], x[col_perez_f2], tiltangle))

    return df
