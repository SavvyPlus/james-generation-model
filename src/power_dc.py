import pandas as pd

from typing import Dict
from .util import col_dc_m2, col_dc_array, col_poa_wm2

SystemLosses = Dict[str, float]


def get_array_area(panel_num: int, area_per_panel: float) -> float:
    """
    Calculates effective POA on panel in W/m2.

    Parameters
    ----------
    panel_num: int
        Panel numbers

    area_per_panel: float
        Area per panel in m2

    Returns
    -------
    array_area : float
        Total panel area in m2

    Notes
    -----

    """
    array_area = panel_num * area_per_panel
    return array_area


def get_power_dc_mw2(lossfactortoggle: int, poa: float, pvefficiency: float,
                     sys_losses: SystemLosses) -> float:
    """
    Calculates effective POA on panel in W/m2.

    Parameters
    ----------
    lossfactortoggle : int
    poa : float
    pvefficiency: float
    sys_losses: SystemLosses

    Returns
    -------
    power_dc : float
        DC power in W/m2

    """
    if lossfactortoggle == 1:
        dc_wm2 = poa * pvefficiency * ((1 - (
                (1 - sys_losses['soiling']) * (1 - sys_losses['shading']) * (
                1 - sys_losses['snow']) * (1 - sys_losses['mismatch']) * (
                        1 - sys_losses['wiring']) * (1 - sys_losses['connections']) * (
                        1 - sys_losses['lid']) * (1 * sys_losses['nameplate']) * (
                        1 - sys_losses['age']) * (1 - sys_losses['availability']))))
    else:
        dc_wm2 = poa * pvefficiency

    return dc_wm2


def get_power_dc_array(dc_wm2: float, array_area: float) -> float:
    """
    Calculates effective POA on panel in W/m2.

    Parameters
    ----------
    dc_wm2 : float
    array_area : float

    Returns
    -------
    power_dc_array : float
        DC power in W/array

    """
    power_dc_array = dc_wm2 * array_area
    return power_dc_array


def power_dc_calculation(df: pd.DataFrame, lossfactortoggle: int, pvefficiency: float,
                         sys_losses: SystemLosses, panel_num: int,
                         area_per_panel: float) -> pd.DataFrame:
    df[col_dc_m2] = df[col_poa_wm2].map(lambda x: get_power_dc_mw2(lossfactortoggle, x,
                                                        pvefficiency, sys_losses))
    array_area = get_array_area(panel_num, area_per_panel)
    df[col_dc_array] = df[col_dc_m2].map(lambda x: get_power_dc_array(x, array_area))
    return df
