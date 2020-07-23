import math
import pandas as pd

from typing import Tuple
from util import col_ib, col_id, col_ir, col_dni, col_dhi, col_solar_zen_ang, col_aoi_deg, col_poa_wm2, col_poa_kwm2

Irradiance = Tuple[float, float, float]


def get_id_val(di: float, dc: float, dh: float) -> float:
    """
    Calculates Id: diffuse on panel W/m2.

    Parameters
    ----------
    di : float
    dc : float
    dh: float

    Returns
    -------
    id_val : float

    """
    id_val = abs(sum([di, dc, dh]))
    return id_val


def get_ir_val(dni: float, dhi: float, zenith: float, tiltangle: float) -> float:
    """
    Calculates Ir: ground reflected irradiance on panel W/m2.

    Parameters
    ----------
    dni: int
    dhi: int
    zenith: float
    tiltangle: float

    Returns
    -------
    ir_val : float

    """
    ir_val = abs(0.2 * (dni * math.cos(math.radians(zenith)) + dhi) *
                 ((1 - math.cos(math.radians(tiltangle))) / 2))
    return ir_val


def get_ib_val(dni: float, aoi: float) -> float:
    """
    Calculates Id: diffuse on panel W/2, Ir: ground reflected irradiance
    on panel W/m2 and Ib: beam irradiance on panel W/m2.

    Parameters
    ----------
    dni: float
    aoi: float

    Returns
    -------
    ib_val : float

    """
    ib_val = abs(dni * math.cos(math.radians(aoi)))
    return ib_val


def get_poa_wm2(id_val: float, ir_val: float, ib_val: float) -> float:
    """
    Calculates effective POA on panel in W/m2.

    Parameters
    ----------
    id_val : float
        Diffuse on panel W/m2

    ir_val : float
        Ground reflected irradiance on panel W/m2

    ib_val: float
        Beam irradiance on panel W/m2

    Returns
    -------
    poa : float
        Effective POA on panel W/m2

    Notes
    -----

    """
    poa = sum([id_val, ir_val, ib_val])
    return poa


def effective_poa_calculation(df: pd.DataFrame, tiltangle: float) -> pd.DataFrame:
    # df[col_id] = df.apply(lambda x: get_id_val(x[col_di], x[col_dc], x[col_dh]), axis=1)
    df[col_ir] = df.apply(lambda x: get_ir_val(x[col_dni], x[col_dhi], x[col_solar_zen_ang], tiltangle), axis=1)
    df[col_ib] = df.apply(lambda x: get_ib_val(x[col_dni], x[col_aoi_deg]), axis=1)
    # df[col_poa_wm2] = df.apply(lambda x: get_poa_wm2(x[col_id], x[col_ir], x[col_ib]), axis=1)
    # df[col_poa_kwm2] = df[col_poa_wm2].map(lambda x: x / 1000)

    return df
