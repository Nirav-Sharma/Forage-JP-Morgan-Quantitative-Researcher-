import pandas as pd
import numpy as np
import datetime as dt

Nat_gas =  pd.read_csv("Nat_Gas (2).csv")
Nat_gas['Dates']=pd.to_datetime(Nat_gas['Dates'])

Nat_gas.set_index('Dates',inplace=True)

i_d = [insert injection dates] #Enter any dates for injection by writing the date in format yyyy-mm-dd and in '' marks seperating each date with a comma
i_p = Nat_gas.loc[i_d]['Prices'] 

w_d = [insert withdrawal dates] #Enter any dates for withdawal by writing the date in format yyyy-mm-dd and in '' marks seperating each date with a comma
w_p = Nat_gas.loc[w_d]['Prices']

i_c =  #Cost of injection. Can be changed
w_c =  #Cost of withdrawal. Can be changed
t_c =  #Cost of transportation. Can be changed
m_i =  #Maximum inventory. Can be changed
m_ir_m =  #Monthly rate of maximum injection. Can be changed
m_w_m =  #Monthly rate of maximum withdrawal. Can be changed
s_c =  #Cost of storage monthly. Can be changed
    
planned_injection = 0

for i in range(0,len(i_p)):
     planned_injection += i_p[i]*m_ir_m

planned_injection  

planned_Withdrawal = 0

for i in range(0,len(w_p)):
     planned_Withdrawal += w_p[i]*m_w_m

Margin = planned_Withdrawal - planned_injection
i_d[0]
w_d[-1]
storage_time = len(pd.date_range(start=i_d[0], end=w_d[-1], freq='M'))
total_storage_cost = storage_time*s_c
 
Net_margin = ( Margin - t_c*(len(w_d)+len(i_d)) - total_storage_cost - i_c*len(i_d) - w_c*len(w_d) )

print(Net_margin)