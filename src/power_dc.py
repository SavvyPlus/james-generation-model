from typing import Dict

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


def get_power_dc(lossfactortoggle: int, poa: float, pvefficiency: float,
                 sys_losses: SystemLosses, panel_num: int,
                 area_per_panel: float) -> float:
    """
    Calculates effective POA on panel in W/m2.

    Parameters
    ----------
    lossfactortoggle : int
    poa : float
    pvefficiency: float
    sys_losses: SystemLosses
    panel_num: int
    area_per_panel: float

    Returns
    -------
    power_dc : float
        DC power in W/array

    Notes
    -----

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

    array_area = get_array_area(panel_num, area_per_panel)
    power_dc = dc_wm2 * array_area
    return power_dc


# sys_los = {
#     'soiling': 0.02,
#     'shading': 0.03,
#     'snow': 0.0,
#     'mismatch': 0.02,
#     'wiring': 0.02,
#     'connections': 0.005,
#     'lid': 0.015,
#     'nameplate': 0.01,
#     'age': 0.0,
#     'availability': 0.02,
# }
#
#
# print(get_power_dc(1, 157.1309608, 0.19, sys_los, 18, 1.50))


