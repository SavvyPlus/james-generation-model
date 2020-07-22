#!/usr/bin/env python
# coding: utf-8

# In[10]:


import pandas as pd
import numpy as np
import math
import time,datetime
import solar_angle_calculations

IO='Solar PV Model Rev1.6.xlsx'
df= pd.read_excel(io=IO)
print(df.iloc[5][1])

def DNI_on_Horizontal(dni):
    if dni>=0:
            DNI=dni
    else:
        DNI=0
    return DNI


def GHI_on_Horizontal(ghi):
    GHI=ghi
    return GHI


def DHI_on_horizontal(DNI,GHI,n):
    if (GHI-(DNI*math.cos(math.radians(solar_angle_calculations.sza_l[n]))))<0:
        DHI=0
    else:
        DHI=GHI-(DNI*math.cos(math.radians(solar_angle_calculations.sza_l[n])))
    return DHI

DNI_L=[]
GHI_L=[]
DHI_L=[]


for i in range(8760):
    DNI=DNI_on_Horizontal(df.iloc[i][1])
    GHI=GHI_on_Horizontal(df.iloc[i][2])
    DHI=DHI_on_horizontal(DNI,GHI,i)
    DNI_L.append(DNI)
    GHI_L.append(GHI)
    DHI_L.append(round(DHI))

k={'TimeStamp':solar_angle_calculations.timestamp_l,'DNI on Horizontal(W/m2)':DNI_L,'DHI on Horizontal(W/m2) ': DHI_L, 'GHI on Horizontal(W/m2)': GHI_L}
                
DNI_DHI_GHI=pd.DataFrame(k)

print(DNI_DHI_GHI)
                
                
                
                


# In[ ]:




