import boto3

client = boto3.client('s3', region_name='ap-southeast-2')

# solar angle columns
col_date = 'Date'
col_hour = 'Hour'
col_julian_day = 'Julian Day'
col_julian_century = 'Julian Century'
col_geom_mean_long_sun = 'Geom Mean Long Sun (deg)'
col_geom_mean_anom_sun = 'Geom Mean Anom Sun (deg)'
col_eccent_earth_orbit = 'Eccent Earth Orbit'
col_sun_equ_centre = 'Sun Equation of Centre'
col_sun_true_long = 'Sun True Long (deg)'
col_sun_app_long = 'Sun App Long (deg)'
col_mean_obliq_ecl = 'Mean Obliq Ecliptic (deg)'
col_oblig_cor = 'Obliq Corr (deg)'
col_sun_dec = 'Sun Declin (deg)'
col_var_y = 'var y'
col_eq_time = 'Eq of Time (minutes)'
col_ha_sunrise = 'HA Sunrise (deg)'
col_solar_noon = 'Solar Noon (LST)'
col_sunrise_time = 'Sunrise Time (LST)'
col_sunset_time = 'Sunset Time (LST)'
col_true_solar_time = 'True Solar Time (min)'
col_hour_ang = 'Hour Angle (deg)'
col_solar_zen_ang = 'Solar Zenith Angle (deg)'
col_solar_elev_ang = 'Solar Elevation Angle (deg)'
col_aprox_atmos_ref = 'Approx Atmospheric Refraction (deg)'
col_solar_elev_cor = 'Solar Elevation correct for atm ref (deg)'
col_solar_azimuth_ang = 'Solar Azimuth Angle (deg cw from N)'

# radiation columns
col_dni = 'DNI on Horizontal (W/m2)'
col_ghi = 'GHI on Horizontal (W/m2)'
col_dhi = 'DHI on Horizontal (W/m2)'

# aoi columns
col_aoi_rad = 'Angle of Incidence (a) rad'
col_aoi_deg = 'Angle of Incidence (AOI) deg'

# Perez columns
col_perez_a = 'Perez - a'
col_perez_b = 'Perez - b'
col_perez_sky = 'Perez - sky clearness e'
col_perez_air_mass_optical = 'Perez - Air Mass optical'
col_perez_delta = 'Perez - delta'
col_perez_f11 = 'Perez - e lookup for F11'
col_perez_f12 = 'Perez - e lookup for F12'
col_perez_f13 = 'Perez - e lookup for F13'
col_perez_f21 = 'Perez - e lookup for F21'
col_perez_f22 = 'Perez - e lookup for F22'
col_perez_f23 = 'Perez - e lookup for F23'
col_perez_f1 = 'Perez - F1'
col_perez_f2 = 'Perez - F2'
col_model = 'Which diffuse model?'
col_di = 'Di W/m2'
col_dc = 'Dc W/m2'
col_dh = 'Dh W/m2'


# irradiance columns
col_id = 'Id = Di + Dc + Dh diffuse on panel W/m2'
col_ir = 'Ir - ground reflected irradiance on panel'
col_ib = 'Ib - beam irradiance on panel W/m2'

# POA columns
col_poa_wm2 = 'Effective POA on panel W/m2'
col_poa_kwm2 = 'Effective POA on panel kW/m2'

# Power DC columns
col_dc_m2 = 'Power DC W/m2'
col_dc_array = 'Power DC W/array'

# Power AC columns
col_ac_w = 'Power AC W'
col_ac_kw = 'Power AC kW'
col_ac_kw_invert_losses = 'Power AC kW inc Inverter losses'

# S3 path format
s3_path = 's3://{}/{}'

def put_file_to_s3(filename, bucket, key, is_public=False):
    with open(filename, "rb") as f:
        if is_public:
            response = client.upload_fileobj(f, bucket, key, ExtraArgs={'ACL': 'public-read'})
        else:
            response = client.upload_fileobj(f, bucket, key)
    return response