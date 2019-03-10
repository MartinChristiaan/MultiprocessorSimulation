import numpy as np

from simulation import get_dims
# import plotly
# import plotly.graph_objs as go
# from plotly import tools

import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

names = ["Bus","Mesh","Torus","Tree"]
plot_names = ["Latency","Sendrate","Number of Links","Number of Routers"]
N = np.arange(4,17)


latencies = [np.ones_like(N),2*np.sqrt(N)/3,np.sqrt(N),2*np.log2(N)]
bisection_bandwidths = [np.ones_like(N)/N,2*np.sqrt(N)/N,2*np.sqrt(N)/N,N*2/N]
num_links = [N,(np.sqrt(N)-1)*2*np.sqrt(N)*2,2*N,np.log2(N)*N*2]
num_routers = [np.ones_like(N),N,N,N-1]


arrs = [latencies,bisection_bandwidths,num_links,num_routers]
markers = ["o","v","^","<",">","1","2","3","4"]
traces = [[],[],[],[]]
layouts = []

f = plt.figure(figsize=(4, 9))
#f,ax_arr = plt.subplots(4, sharex=True)
for j,arr in enumerate(arrs):

    # print(j+1)
    #ax = ax_arr[j]
    plt.subplot(len(arrs),1,j+1)
    for i,val in enumerate(arr):        
        plt.plot(N,val,label = names[i], marker=markers[i])
    plt.ylabel(plot_names[j])
    plt.xlabel("N")
    plt.grid(1)
    plt.legend()
    
#f.subplots_adjust(hspace=0)
    #plt.savefig(plot_names[j].replace(' ','') + ".eps")
plt.tight_layout()
#plt.show()

t_proc = 0.00040
sendrate_bus = 1/(N*t_proc)
latency_bus = N/2 * t_proc

ni_transfer_delay = 0.0005
router_processing_time = 0.0006
FifoProcessingTime = 0.00025

sendrate_mesh = 2*np.sqrt(N)/(FifoProcessingTime+ni_transfer_delay+router_processing_time)/N
avg_dist_mesh = (2*np.sqrt(N)/3)
latency_mesh = (avg_dist_mesh + 1) * (router_processing_time + FifoProcessingTime)   + 2*ni_transfer_delay + router_processing_time


sendrate_torus = 2*np.sqrt(N)/(ni_transfer_delay+router_processing_time*2 + FifoProcessingTime*2)/N
avg_dist_torus = np.sqrt(N)
latency_torus = (avg_dist_torus + 1) * (router_processing_time + FifoProcessingTime)*2   + 2*ni_transfer_delay + router_processing_time*2
 


latencies = [latency_bus,latency_mesh,latency_torus]
sendrates = [sendrate_bus,sendrate_mesh,sendrate_torus]
arrs = [latencies,sendrates]
plot_names = ["Latency","Sendrate"]
f = plt.figure(figsize=(4, 5))
#f,ax_arr = plt.subplots(4, sharex=True)
for j,arr in enumerate(arrs):

    # print(j+1)
    #ax = ax_arr[j]
    plt.subplot(len(arrs),1,j+1)
    for i,val in enumerate(arr):        
        plt.plot(N,val,label = names[i], marker=markers[i])
    plt.ylabel(plot_names[j])
    plt.xlabel("N")
    plt.grid(1)
    plt.legend()


    # layouts.append(dict(title = plot_names[j],
    #           yaxis = dict(title = plot_names[j]),
    #           xaxis = dict(title = "N")))

    # fig = dict(data =traces[j],layout = layouts[j])
    # plotly.offline.plot(fig, auto_open=True,filename=plot_names[j])
plt.tight_layout()
plt.show()