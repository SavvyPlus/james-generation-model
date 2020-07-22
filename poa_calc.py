import math

from typing import Tuple

Irradiance = Tuple[float, float, float]


def get_irradiance(di: float, dc: float, dh: float, dni: int, dhi: int,
                   zenith: float, tiltangle: int, aoi: float) -> Irradiance:
    """
    Calculates Id: diffuse on panel W/2, Ir: ground reflected irradiance
    on panel W/m2 and Ib: beam irradiance on panel W/m2.

    Parameters
    ----------
    di : float
    dc : float
    dh: float
    dni: int
    dhi: int
    zenith: float

    Returns
    -------
    Irradiance : Irradiance
        Irradiance tuple consists of Id, Ir and Ib.

    Notes
    -----

    """
    id_val = abs(sum([di, dc, dh]))
    ir_val = abs(0.2 * (dni * math.cos(math.radians(zenith)) + dhi) * (
            (1 - math.cos(math.radians(tiltangle))) / 2))
    ib_val = abs(dni * math.cos(math.radians(aoi)))
    return id_val, ir_val, ib_val


def get_effective_poa(id_val: float, ir_val: float, ib_val: float) -> float:
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


# id_v, ir_v, ib_v = get_irradiance(155.1378063, 0, -6.197917339, 39, 177, 71.74265435, 28, 80.97277871)
# print(get_effective_poa(id_v, ir_v, ib_v))
