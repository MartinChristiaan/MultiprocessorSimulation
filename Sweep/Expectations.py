import numpy as np

from simulation import get_dims
# import plotly
# import plotly.graph_objs as go
# from plotly import tools

import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

names = ["Bus","Mesh","Torus","Tree"]
plot_names = ["Latency","Bisection Bandwidth","Number of Links","Number of Routers"]
N = np.arange(4,17)


latencies = [np.ones_like(N),2*np.sqrt(N)/3,np.sqrt(N),2*np.log2(N)]
bisection_bandwidths = [np.ones_like(N),2*np.sqrt(N),2*np.sqrt(N),N*2]
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


sendrate_bus = 5/N
latency_bus = N/5

sendrate_mesh = 2*np.sqrt(N)/N
latency_mesh = 2*np.sqrt(N)/3

sendrate_torus = np.sqrt(N)/N
latency_torus = 2*np.sqrt(N)



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