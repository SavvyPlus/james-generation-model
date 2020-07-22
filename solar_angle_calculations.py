#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import math
import time,datetime


latitude=-37.67
longitude=144.85
GMT=10
IO='Solar PV Model Rev1.6.xlsx'
df= pd.read_excel(io=IO)


def timetrans(stamp):
    delta=stamp-pd.to_datetime('1899-12-30 00:00:00')  
    timed=delta.total_seconds()/86400
    date=int(timed)
    hour=timed-int(date)
    return date,hour

def julian_day(date,hour):
    jd=date+2415018.5+hour-GMT/24
    return jd

def julian_century(jd):
    jc=(jd - 2451545) / 36525
    return round(jc,8)

def greenwich_mean_long_sun(jc):
    return (280.46646 + jc*(36000.76983+jc*0.0003032))%360   ##Geom Mean Long Sun (deg)

def geom_mean_anom_sun(jc):
    gmas=357.52911+jc*(35999.05029 - 0.0001537*jc) ##Geom Mean Long Sun (deg)
    return gmas

def eccent_earth_orbit(jc):
    eeo=0.016708634-jc*(0.000042037+0.0000001267*jc)
    return eeo

def sun_equation_of_centre(jc):
    seoc=math.sin(math.radians(gmas))*(1.914602-jc*(0.004817+0.000014*jc))+math.sin(math.radians(2*gmas))*(0.019993-0.000101*jc)+math.sin(math.radians(3*jc))*0.000289
    return seoc

def sun_true_long(gmls,seoc):
    return gmls+seoc

def sun_app_long(jc,stl):
    return stl-0.00569-0.00478*math.sin(math.radians(125.04-1934.136*jc))

def mean_obliq_ecliptic(jc):
    moe=23+(26+((21.448-jc*(46.815+jc*(0.00059-jc*0.001813))))/60)/60
    return moe

def obliq_corr(jc,moe):
    oc=moe+0.00256*math.cos(math.radians(125.04-1934.136*jc))
    return oc

def sun_declin(sal,oc):
    sd=math.degrees(math.asin(math.sin(math.radians(oc))*math.sin(math.radians(sal))))
    return sd

def var_y(oc):
    vy=math.tan(math.radians(oc/2))*math.tan(math.radians(oc/2))
    return vy

def eq_of_time(vy,gmls,eeo,gmas):
    eot=4*math.degrees(vy*math.sin(2*math.radians(gmls))-2*eeo*math.sin(math.radians(gmas))+4*eeo*vy*math.sin(math.radians(gmas))*math.cos(2*math.radians(gmls))
                       -0.5*vy*vy*math.sin(4*math.radians(gmls))-1.25*eeo*eeo*math.sin(2*math.radians(gmas)))
    return eot

def HA_sunrise(sd):
    hs=math.degrees(math.acos(math.cos(math.radians(90.833))/(math.cos(math.radians(latitude))*math.cos(math.radians(sd)))-math.tan(math.radians(latitude))*math.tan(math.radians(sd))))
    return hs

def solar_noon(eot):
    sn=(720-4*longitude-eot+GMT*60)*60     #total seconds
    snh=int(sn/3600)               #  hours
    snm=int((sn-snh*3600)/60)      #minutes
    sns=round(sn-snh*3600-snm*60)   #seconds
    return sn,snh,snm,sns
    
def sunrise_time(sn,hs):
    st=sn-hs*4*60         #total seconds
    sth=int(st/3600)       #  hours
    stm=int((st-sth*3600)/60)      #minutes
    sts=round(st-sth*3600-stm*60)   #seconds
    return st,sth,stm,sts

def sunset_time(sn,hs):
    sst=sn+hs*4*60      #total seconds
    ssth=int(sst/3600)       #  hours
    sstm=int((sst-ssth*3600)/60)      #minutes
    ssts=round(sst-ssth*3600-sstm*60)   #seconds
    return sst,ssth,sstm,ssts

def true_solar_time(hour,eot):
    tst=(hour*1440+eot+4*longitude-60*GMT)%1440
    return tst
    
def hour_angle(tst):
    if (tst/4)<0:
        ha=(tst/4)+180
    else:
        ha=(tst/4)-180
    return ha

def solar_zenith_angle(sd,ha):
    sza=math.degrees(math.acos(math.sin(math.radians(latitude))*math.sin(math.radians(sd))+math.cos(math.radians(latitude))*math.cos(math.radians(sd))*math.cos(math.radians(ha))))
    return sza

def solar_elevation_angle(sza):
    sea=90-sza
    return sea
    
def approx_atmospheric_refraction(sea):
    if sea>85:
        aar=0
    elif sea<=85 and sea>5:
        aar=58.1/(math.tan(math.radians(sea)))-(0.07/(math.tan(math.radians(sea)**3))+(0.000086/(math.tan(math.radians(sea))**5)))
    elif sea<=5 and sea>-0.575:
         aar=1735+sea*(-518.2+sea*(103.4+sea*(-12.79+sea*0.711)))
    else:
        aar= -20.772/math.tan(math.radians(sea))
    aar=aar/3600
    return aar    
    
def solar_elevation_correct_for_atm_ref(sea,aar):
    sec=sea+aar
    return sec

def solar_azimuth_angle(ha,sza,sd):
    if ha>0:
        saa=(math.degrees(math.acos(((math.sin(math.radians(latitude))*math.cos(math.radians(sza)))-math.sin(math.radians(sd)))/(math.cos(math.radians(latitude))*math.sin(math.radians(sza)))))+180)%360
    else:
        saa=(540-math.degrees(math.acos(((math.sin(math.radians(latitude))*math.cos(math.radians(sza)))-math.sin(math.radians(sd)))/(math.cos(math.radians(latitude))*math.sin(math.radians(sza))))))%360
    return saa    
    

timestamp_l=[]
jd_l=[]
jc_l=[]
gmls_l=[]
gmas_l=[]
eeo_l=[]
seoc_l=[]
stl_l=[]
sal_l=[]
moe_l=[]
oc_l=[]
sd_l=[]
vy_l=[]
eot_l=[]
hs_l=[]
sn_l=[]
st_l=[]
sst_l=[]
tst_l=[]
ha_l=[]
sza_l=[]
sea_l=[]
aar_l=[]
sec_l=[]
saa_l=[]


for i in range(8760):
    stamp=df.iloc[i][0]                  #timestamp    
    date,hour=timetrans(stamp)
    jd=julian_day(date,hour)   
    jc=julian_century(jd)
    gmls=greenwich_mean_long_sun(jc)
    gmas=geom_mean_anom_sun(jc)
    eeo=eccent_earth_orbit(jc)
    seoc= sun_equation_of_centre(jc)
    stl=sun_true_long(gmls,seoc)
    sal=sun_app_long(jc,stl)
    moe= mean_obliq_ecliptic(jc)
    oc= obliq_corr(jc,moe)
    sd=sun_declin(sal,oc)
    vy=var_y(oc)
    eot= eq_of_time(vy,gmls,eeo,gmas)
    hs=HA_sunrise(sd)
    sn,snh,snm,sns=solar_noon(eot)
    st,sth,stm,sts=sunrise_time(sn,hs)
    sst,ssth,sstm,ssts=sunset_time(sn,hs)
    tst=true_solar_time(hour,eot)
    ha=hour_angle(tst)
    sza=solar_zenith_angle(sd,ha)
    sea=solar_elevation_angle(sza)
    aar=approx_atmospheric_refraction(sea)
    sec= solar_elevation_correct_for_atm_ref(sea,aar)
    saa=solar_azimuth_angle(ha,sza,sd)
    timestamp_l.append(stamp)
    jd_l.append(jd)
    jc_l.append(jc)
    gmls_l.append(gmls)
    gmas_l.append(gmas)
    eeo_l.append(eeo)
    seoc_l.append(seoc)
    stl_l.append(stl)
    sal_l.append(sal)
    moe_l.append(moe)
    oc_l.append(oc)
    sd_l.append(sd)
    vy_l.append(vy)
    eot_l.append(eot)
    hs_l.append(hs)
    sn_l.append(str(snh)+' :'+str(snm)+' :'+str(sns))
    st_l.append(str(sth)+' :'+str(stm)+' :'+str(sts))
    sst_l.append(str(ssth)+' :'+str(sstm)+' :'+str(ssts))
    tst_l.append(tst)
    ha_l.append(ha)
    sza_l.append(sza)
    sea_l.append(sea)
    aar_l.append(aar)
    sec_l.append(sec)
    saa_l.append(saa) 
    
d = {'TimeStamp': timestamp_l ,'Julian Day': jd_l, 'Julian Century': jc_l, 'greenwich_mean_long_sun': gmls_l, 'eom_mean_anom_sun':gmas_l,'eccent_earth_orbit': eeo_l,
     'sun_equation_of_centre': seoc_l,'sun_ture_long': stl_l,'sun_app_long': sal_l,'mean_obliq_ecliptic': moe_l,'obliq_corr': oc_l,'sun_declin': sd_l,
     'var_y': vy_l,'eq_of_time': eot_l,'HA_sunrise': hs_l,'solar_noon':sn_l,'sunrise_time': st_l,'sunset_time': sst_l,'true_solar_time': tst_l,'hour_angle': ha_l,
    'solar_zenith_angle(deg)': sza_l,'solar_elevation_angle(deg)': sea_l,'approx_atmospheric_refraction(deg)': aar_l,'solar_elevation_correct_for_atm_ref(deg)': sec_l,
    'solar_azimuth_angle': saa_l}

solar_angle_cal=pd.DataFrame(d)
print(solar_angle_cal)


# In[ ]:





# In[ ]:




