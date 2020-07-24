import json
import os
import pandas as pd
from src.solar_angle_calculations import calculate_angle
from src.radiation_calculation import calculate_radiation
from src.aoi_calculation import aoi_calculation
from src.perez_model import perez
from src.poa_calc import effective_poa_calculation
from src.power_dc import power_dc_calculation
from src.power_ac import power_ac_calculation
from src.util import *


def lambda_handler(event, context):
    latitude = event["latitude"]
    longitude = event["longitude"]
    GMT = event["GMT"]
    orientation = event['orientation']
    tiltangle = event['tiltangle']
    lossfactortoggle = event['lossfactortoggle']
    pvefficiency = event['pvefficiency']
    panel_num = event['panel_num']
    area_per_panel = event['area_per_panel']
    invertsize = event['invertsize']
    invertefficiency = event['invertefficiency']
    sys_losses = {
        'soiling': 0.02,
        'shading': 0.03,
        'snow': 0.0,
        'mismatch': 0.02,
        'wiring': 0.02,
        'connections': 0.005,
        'lid': 0.015,
        'nameplate': 0.01,
        'age': 0.0,
        'availability': 0.02,
    }
    if 'sys_losses' in event.keys():
        sys_losses = event['sys_losses']

    bucket = event['bucket']
    key = event['key']
    file_path = s3_path.format(bucket, key)
    print(file_path)
    df = pd.read_csv(file_path, parse_dates=['TimeStamp'])
    print(df)
    # calculate solar angle
    df = calculate_angle(df, latitude, longitude, GMT)

    # normalize solar radiation data
    df = calculate_radiation(df)

    # calculate angle of incidence (AOI)
    df = aoi_calculation(df, orientation, tiltangle)

    # run perez model
    df = perez(df, tiltangle)

    # calculate effective poa
    df = effective_poa_calculation(df, tiltangle)

    # calculate power DC
    df = power_dc_calculation(df, lossfactortoggle, pvefficiency, sys_losses, panel_num,
                              area_per_panel)

    # calculate final power AC
    df = power_ac_calculation(df, invertsize, invertefficiency)
    local_path = '{}-final.csv'.format(key)
    df.to_csv(f'/tmp/{local_path}', index=False)
    print(put_file_to_s3(f'/tmp/{local_path}', bucket, local_path))

    return {
        'statusCode': 200,
        'body': json.dumps('Calculation finished.')
    }


if __name__ == '__main__':
    event = {
        'latitude': -37.67,
        'longitude': 144.85,
        'GMT': 10,
        'orientation': 0,
        'tiltangle': 28,
        'lossfactortoggle': 1,
        'pvefficiency': 0.19,
        'panel_num': 18,
        'area_per_panel': 1.5,
        'invertsize': 5.25,
        'invertefficiency': 0.96,
        'sys_losses': {
            'soiling': 0.02,
            'shading': 0.03,
            'snow': 0.0,
            'mismatch': 0.02,
            'wiring': 0.02,
            'connections': 0.005,
            'lid': 0.015,
            'nameplate': 0.01,
            'age': 0.0,
            'availability': 0.02,
        },
        'bucket': 'solar-radiation',
        'key': '-37.583333_144.1_Solcast_PT60M.csv'
    }

    lambda_handler(event, None)