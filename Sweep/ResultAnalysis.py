import pandas as pd
from plotter import *
import matplotlib.pyplot as plt
from simulation import readLog
import os
import numpy as np
df = pd.read_csv("results/Final_result.csv")
filter_vals = [("Load Value",0.95)]
LoadValue = "Load Value"
#@anti_filter = [("Load Value",0.15)]
NumberOfNodes = "NumberOfNodes"
LatencyAverage = "Latency Average"
SendrateAverage = "Sendrate Average" 
 
NIBufferCapacity = "NIBufferCapacity"
Interconnect = "Interconnect"
df_filt = filter_df(df,eq_filter=[(LoadValue,0.95)])
interconnectsdf,ics = seperate_dim(df_filt,Interconnect)

for k,ic in enumerate(interconnectsdf):
    create_figure()
    plot_traces(ic,NumberOfNodes,LatencyAverage,NIBufferCapacity)
    plt.savefig("figures/" + ics[k] + "LatBufCap.eps")
    plot_traces(ic,NumberOfNodes,SendrateAverage,NIBufferCapacity)
    plt.savefig("figures/" + ics[k] + "SendRateBufCap.eps")

eq_filter = [(NIBufferCapacity,2)]
neq_filter = [(LoadValue,0.15),(LoadValue,0.65),(LoadValue,0.45)]
df_filt = filter_df(df,eq_filter=eq_filter,neq_filter = neq_filter)

# df = pd.read_csv("results/Final_result.csv")
# filter_vals = [("NIBufferCapacity",2)]
# anti_filter = [("Load Value",0.15),("Load Value",0.65),("Load Value",0.45)]
# title_fun = lambda load :  "Load : " + str(load)
#x_dim = "NumberOfNodes"
#y_dims = ["Latency Average","Sendrate Average"]

dfs_loadval,loadvals = seperate_dim(df_filt,LoadValue)
for k,df_load in enumerate(dfs_loadval):
    create_figure()
    plot_traces(df_load,NumberOfNodes,LatencyAverage,Interconnect)
    plt.savefig("figures/" + str(loadvals[k]) + "LatencyInterconnect.eps")
    plot_traces(df_load,NumberOfNodes,SendrateAverage,Interconnect)
    plt.savefig("figures/" + str(loadvals[k]) + "SendrateInteconnect.eps")
    
plt.show()
# trace_dim = "Interconnect"
# plot_dim = "Load Value"
# plotter.plot_df(df,plot_dim,trace_dim,x_dim,y_dims,_filter=filter_vals,anti_filter=anti_filter,title_fun=title_fun)



# ## LAtency distribution analysis

# def parse_results(nrNodes,output_directory):    
#     latency_names = ["Latency Average","Latency Min","Latency Max"]
#     sendrate_names = ["Sendrate Average","Sendrate Min","Sendrate Max"]
#     latency = []
#     sendrate = []
#     for i in range(1, nrNodes + 1):
#         latency += [readLog(os.path.join(output_directory, "latency"+str(i)) + ".log")]
#         sendrate += [readLog(os.path.join(output_directory, "sendrate"+str(i)) + ".log")]
#     return latency,sendrate

# load_values = df[plot_dim].unique()
# load_values.sort()
# NIBufferCapacity = 2.0
# latency_arr = []
# sendrate_arr = []
# nrNodes = 4
# topos = ["Mesh","Torus"]

# plt.figure()
# for k, topo in enumerate(topos):
#     latency_arr = []
#     sendrate_arr = []
#     for load_value in load_values:
#         output_directory_template = topo +'/nrNodes_' + str(nrNodes) + "_load_" + str(load_value) + "_bufcap_" + str(NIBufferCapacity)
#         output_directory = os.path.abspath(output_directory_template)
#         latency,sendrate = parse_results(nrNodes,output_directory)
#         latency_arr.append(latency)
#         sendrate_arr.append(sendrate)
#     latency_arr = np.array(latency_arr)
#     sendrate_arr = np.array(sendrate_arr)

#     markers = ["o","v","^","<",">","1","2","3","4"]
#     ax = plt.subplot(2,2,k*2+1)
#     ax.set_title(topo)
#     for i in range(latency_arr.shape[1]):
#         plt.plot(load_values,latency_arr[:,i],label = "Node : " + str(i),marker = markers[i])
#     plt.legend()
#     plt.xlabel("Load")
#     plt.grid(1)
#     plt.ylabel("Latency")
    
#     ax = plt.subplot(2,2,k*2+2)
#     ax.set_title(topo)
#     for i in range(sendrate_arr.shape[1]):
#         plt.plot(load_values,sendrate_arr[:,i],label = "Node : " + str(i),marker = markers[i])
#     plt.legend()
#     plt.xlabel("Load")
#     plt.grid(1)
#     plt.ylabel("Sendrate")

# plt.show()












