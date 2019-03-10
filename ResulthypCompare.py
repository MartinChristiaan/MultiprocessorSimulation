import pandas as pd
from plotter import *
import matplotlib.pyplot as plt
from simulation import readLog
import os
import numpy as np
df = pd.read_csv("results/Final_result.csv")
# Dataframe indexes
LoadValue = "Load Value"
NumberOfNodes = "NumberOfNodes"
LatencyAverage = "Latency Average"
SendrateAverage = "Sendrate Average" 
NIBufferCapacity = "NIBufferCapacity"
Interconnect = "Interconnect"
# Model parameters
t_proc = 0.00040
ni_transfer_delay = 0.0005
router_processing_time = 0.0006
FifoProcessingTime = 0.00025
#Sendrate Comparison


calc_bus_sr = lambda N : 1/(N*t_proc)
calc_mesh_sr = lambda N : 2*np.sqrt(N)/(FifoProcessingTime+ni_transfer_delay+router_processing_time)/N 
calc_torus_sr = lambda N : 2*np.sqrt(N)/(ni_transfer_delay+router_processing_time*2 + FifoProcessingTime*2)/N 

calc_bus_l = lambda N : N/2 * t_proc
avg_dist_mesh  = lambda N : (2*np.sqrt(N)/3)
avg_dist_torus = lambda N : np.sqrt(N)
calc_mesh_l = lambda N : (avg_dist_mesh(N) + 1) * (router_processing_time + FifoProcessingTime)   + 2*ni_transfer_delay + router_processing_time
calc_torus_l =lambda N : (avg_dist_torus(N) + 1) * (router_processing_time + FifoProcessingTime)*2   + 2*ni_transfer_delay + router_processing_time*2

calc_sr_arr = [calc_bus_sr,calc_mesh_sr,calc_torus_sr]
calc_l_arr = [calc_bus_l,calc_mesh_l,calc_torus_l]
sendrates = []
latencies = []

df_filt = filter_df(df,eq_filter=[(LoadValue,0.95),(NIBufferCapacity,2)])
df_filt = df_filt.sort_values(by=[NumberOfNodes])

interconnectsdf,ics = seperate_dim(df_filt,Interconnect)

for i,ic_df in enumerate(interconnectsdf):
    sr=[abs(calc_sr_arr[i](row[NumberOfNodes]) - row[SendrateAverage])/row[SendrateAverage] * 100 for _,row in ic_df.iterrows()]

    sendrates.append(sr)


df_filt = filter_df(df,eq_filter=[(LoadValue,0.25),(NIBufferCapacity,2)])
df_filt = df_filt.sort_values(by=[NumberOfNodes])

interconnectsdf,ics = seperate_dim(df_filt,Interconnect)

for i,ic_df in enumerate(interconnectsdf):
    latencies.append([abs(calc_l_arr[i](row[NumberOfNodes]) - row[LatencyAverage])/calc_l_arr[i](row[NumberOfNodes]) * 100 for _,row in ic_df.iterrows()])
    print(np.mean(latencies[i]))

N = df_filt[NumberOfNodes].unique()

# Mesh latency is overestimated
# Bus latency is overestimated


plt.figure()
for sr in sendrates:
    plt.plot(N,sr)
plt.xlabel(NumberOfNodes)
plt.ylabel("Sendrate Error")
plt.grid(1)
plt.show()


plt.figure()
for l in latencies:
    plt.plot(N,l)
plt.xlabel(NumberOfNodes)
plt.ylabel("Latency Error")
plt.grid(1)
plt.show()


# ## Latency distribution analysis








