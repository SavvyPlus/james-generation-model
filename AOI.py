import math
def AOI(orient:float,tilt:float,zenith:float,azimuth:float):
    AOI_rad=math.sin(math.radians(zenith))*math.cos(math.radians(azimuth-orient))*math.sin(math.radians(tilt))\
    +math.cos(math.radians(z))*math.cos(math.radians(tilt))
    AOI_deg=math.degrees(math.acos(AOI_rad))
return AOI_rad,AOI_deg 
AOI()
  
