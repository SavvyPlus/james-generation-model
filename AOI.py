import math

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

def AOI(orient:float,tilt:float,zenith:float,azimuth:float):
    
    AOI_rad=math.sin(math.radians(zenith))*math.cos(math.radians(azimuth-orient))*math.sin(math.radians(tilt))\
    +math.cos(math.radians(z))*math.cos(math.radians(tilt))
    AOI_deg=math.degrees(math.acos(AOI_rad))
    return AOI_rad,AOI_deg 

# AOI_rad,AOI_deg=AOI(0,28,116.122,201.302)
# print(AOI_rad)
# print(AOI_deg)
  
