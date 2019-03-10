import pandas as pd
from plotter import *
import matplotlib.pyplot as plt
from simulation import readLog
import os
import numpy as np
df = pd.read_csv("results/buffercaptest.csv")
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

def make_fig(names,dataframes,xdim,ydim,tracedim):
    for k,df in enumerate(dataframes):
        create_figure()
        plot_traces(df,xdim,ydim,tracedim)
        plt.savefig("figures/" + str(names[k]).replace(" ",'') +ydim.replace(" ",'')+tracedim.replace(" ",'')+".eps")
    
#df_filt = filter_df(df,eq_filter=eq_filter,neq_filter = neq_filter)
make_fig(ics,interconnectsdf,NumberOfNodes,LatencyAverage,NIBufferCapacity)
make_fig(ics,interconnectsdf,NumberOfNodes,SendrateAverage,NIBufferCapacity)


eq_filter = [(NIBufferCapacity,2)]
neq_filter = [(LoadValue,0.15),(LoadValue,0.65),(LoadValue,0.45)]

df_filt = filter_df(df,eq_filter,neq_filter)
dfs_loadval,loadvals = seperate_dim(df_filt,LoadValue)
make_fig(loadvals,dfs_loadval,NumberOfNodes,SendrateAverage,Interconnect)
make_fig(loadvals,dfs_loadval,NumberOfNodes,LatencyAverage,Interconnect)

## LAtency distribution analysis

df = pd.read_csv("results/ContLoadTest.csv")
def parse_results(nrNodes,output_directory):    
    latency_names = ["Latency Average","Latency Min","Latency Max"]
    sendrate_names = ["Sendrate Average","Sendrate Min","Sendrate Max"]
    latency = []
    sendrate = []
    for i in range(1, nrNodes + 1):
        latency += [readLog(os.path.join(output_directory, "latency"+str(i)) + ".log")]
        sendrate += [readLog(os.path.join(output_directory, "sendrate"+str(i)) + ".log")]
    return latency,sendrate

load_values = df[LoadValue].unique()
load_values.sort()
NIBufferCapacity = 2.0
latency_arr = []
sendrate_arr = []
nrNodes = 9
topos = ["Mesh","Torus","Bus"]

def get_dist(p1,p2):
    x1,y1= p1
    x2,y2 = p2
    dx = x1-x2
    dy = y1 - y2
    return np.sqrt( dx*dx + dy * dy)
     

for k, topo in enumerate(topos):
    latency_arr = []
    sendrate_arr = []
    for load_value in load_values:
        output_directory_template = topo +'/nrNodes_' + str(9.0) + "_load_" + str(load_value) + "_bufcap_" + str(NIBufferCapacity)
        output_directory = os.path.abspath(output_directory_template)
        latency,sendrate = parse_results(nrNodes,output_directory)
        latency_arr.append(latency)
        sendrate_arr.append(sendrate)
    latency_arr = np.array(latency_arr)
    sendrate_arr = np.array(sendrate_arr)

    markers = ["o","v","^","<",">","1","2","3","4"]
    plt.figure(figsize=(4.5,3.5))
    annotate_pos = []
    xmax = 0
    for i in range(latency_arr.shape[1]):
        plt.plot(load_values,latency_arr[:,i],label = str(i+1),marker = markers[i])
        line_end = load_values[-1], latency_arr[-1,i]
        text_pos= line_end[0] + 0.1,line_end[1]
        for ap in annotate_pos:
            if get_dist(text_pos,ap) < 0.1:
                text_pos = text_pos[0] + 0.02,text_pos[1]
        annotate_pos.append(text_pos)
        if text_pos[0] > xmax:
            xmax =text_pos[0]
        # plt.annotate(str(i), xy=line_end,  xycoords='data',textcoords = 'data',
        #         xytext=text_pos ,horizontalalignment='right', verticalalignment='top',
        #         arrowprops=dict(arrowstyle="simple", connectionstyle="arc3")
        #         )

    plt.legend()
    plt.xlabel("Load")
    plt.grid(1)
    plt.ylabel("Latency")
    plt.xlim([0.2,xmax])
    plt.tight_layout()
    plt.savefig("figures/LatPerNode_"+topo+".eps")

    plt.figure(figsize=(4.5,3.5))

    for i in range(sendrate_arr.shape[1]):
        plt.plot(load_values,sendrate_arr[:,i],label = str(i+1),marker = markers[i])
        line_end = load_values[-1], sendrate_arr[-1,i]
        # plt.annotate(str(i), xy=line_end,  xycoords='data',textcoords = 'data',
        #         xytext=(line_end[0] + np.sin(i) * 0.01 + 0.1,line_end[1]) ,horizontalalignment='right', verticalalignment='top',
        #         arrowprops=dict(arrowstyle="simple", connectionstyle="arc3")
        #         )
    plt.legend()
    plt.xlabel("Load")
    #plt.xlim([0.2,1.05])
    plt.grid(1)
    plt.ylabel("Sendrate")
    plt.tight_layout()
    plt.savefig("figures/SRPerNode_"+topo+".eps")

plt.show()












