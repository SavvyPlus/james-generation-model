
import pandas as pd
import numpy as np
import math
import time,datetime
from .util import *


def calculate_angle(df: pd.DataFrame, latitude: float, longitude: float, GMT: int) -> pd.DataFrame:
    """ Calculate solar angle based on time stamp
    :param df: dataframe with TimeStamp column of pd.TimeStamp type
        """

    def get_date(stamp):
        delta = stamp - pd.to_datetime('1899-12-30 00:00:00')
        timed = delta.total_seconds() / 86400
        return int(timed)

    def get_hour(stamp):
        delta = stamp - pd.to_datetime('1899-12-30 00:00:00')
        timed = delta.total_seconds() / 86400
        date = int(timed)
        return timed - date

    def julian_day(date, hour):
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

    def sun_equation_of_centre(jc, gmas):
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




    df[col_date] = df['TimeStamp'].map(get_date)
    df[col_hour] = df['TimeStamp'].map(get_hour)
    df[col_julian_day] = df.apply(lambda x: julian_day(x[col_date], x[col_hour]), axis=1)
    df[col_julian_century] = df[col_julian_day].map(julian_century)
    df[col_geom_mean_long_sun] = df[col_julian_century].map(greenwich_mean_long_sun)
    df[col_geom_mean_anom_sun] = df[col_julian_century].map(geom_mean_anom_sun)
    df[col_eccent_earth_orbit] = df[col_julian_century].map(eccent_earth_orbit)
    df[col_sun_equ_centre] = df.apply(lambda x: sun_equation_of_centre(x[col_julian_century],
                                                                       x[col_geom_mean_anom_sun]), axis=1)
    df[col_sun_true_long] = df.apply(lambda x: sun_true_long(x[col_geom_mean_long_sun], x[col_sun_equ_centre]), axis=1)
    df[col_sun_app_long] = df.apply(lambda x: sun_app_long(x[col_julian_century], x[col_sun_true_long]), axis=1)
    df[col_mean_obliq_ecl] = df[col_julian_century].map(mean_obliq_ecliptic)
    df[col_oblig_cor] = df.apply(lambda x: obliq_corr(x[col_julian_century], x[col_mean_obliq_ecl]), axis=1)
    df[col_sun_dec] = df.apply(lambda x: sun_declin(x[col_sun_app_long], x[col_oblig_cor]), axis=1)
    df[col_var_y] = df[col_oblig_cor].map(var_y)
    df[col_eq_time] = df.apply(lambda x: eq_of_time(x[col_var_y],
                                                    x[col_geom_mean_long_sun],
                                                    x[col_eccent_earth_orbit],
                                                    x[col_geom_mean_anom_sun]),
                               axis=1)
    df[col_ha_sunrise] = df[col_sun_dec].map(HA_sunrise)
    df[col_true_solar_time] = df.apply(lambda x: true_solar_time(x[col_hour], x[col_eq_time]), axis=1)
    df[col_hour_ang] = df[col_true_solar_time].map(hour_angle)
    df[col_solar_zen_ang] = df.apply(lambda x: solar_zenith_angle(x[col_sun_dec], x[col_hour_ang]), axis=1)
    df[col_solar_elev_ang] = df[col_solar_zen_ang].map(solar_elevation_angle)
    df[col_aprox_atmos_ref] = df[col_solar_elev_ang].map(approx_atmospheric_refraction)
    df[col_solar_elev_cor] = df.apply(lambda x: solar_elevation_correct_for_atm_ref(x[col_solar_elev_ang],
                                                                                    x[col_aprox_atmos_ref]), axis=1)
    df[col_solar_azimuth_ang] = df.apply(lambda x: solar_azimuth_angle(x[col_hour_ang],
                                                                       x[col_solar_zen_ang],
                                                                       x[col_sun_dec]), axis=1)
    return df
