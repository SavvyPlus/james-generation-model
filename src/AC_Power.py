#Inverter data
inv_size=5.2; 
inv_eff=96; 

"""
Description:

This is a function used to compute AC power from an inverter for a given solar panel. 

Inputs:

Calculated DC Power obtained from solar panel in Watts
Inverter Size in kW
Inverter Efficiency in % 

Outputs:

AC Power in Watts
AC Power in kW
AC Power including losses in kW

"""
def AC_power(DC_Power:float,inv_size:float,inv_eff:float):
    ac_power=min(DC_Power,inv_size*1000)
    ac_power_kW=ac_power/1000;
    ac_kW_WithLoss=ac_power_kW*inv_eff/100;
    return ac_power,ac_power_kW,ac_kW_WithLoss
    
