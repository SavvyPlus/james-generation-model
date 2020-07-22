inv_size=5.2;
inv_eff=0.96;
def AC_power(DC_Power:float,inv_size:float,inv_eff:float):
    ac_power=min(DC_Power,inv_size*1000)
    ac_power_kW=ac_power/1000;
    ac_kW_WithLoss=ac_power_kW*inv_eff;
    return ac_power,ac_power_kW,ac_kW_WithLoss
    
