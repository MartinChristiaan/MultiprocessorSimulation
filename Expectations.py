import numpy as np


# import plotly
# import plotly.graph_objs as go
# from plotly import tools

import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

names = ["Bus","Mesh","Torus","Tree"]
plot_names = ["Latency","Bisection Bandwidth","Number of Links","Number of Routers"]
N = np.arange(0,33)

latencies = [np.ones_like(N),2*np.sqrt(N)/3,np.sqrt(N)/2,2*np.log2(N)]
bisection_bandwidths = [np.ones_like(N),np.sqrt(N),2*np.sqrt(N),N*2]
num_links = [N,(np.sqrt(N)-1)*2*np.sqrt(N),2*N,np.log2(N)*N*2]
num_routers = [np.ones_like(N),N,N,N-1]


arrs = [latencies,bisection_bandwidths,num_links,num_routers]
markers = ["o","v","^","<",">","1","2","3","4"]
traces = [[],[],[],[]]
layouts = []
for j,arr in enumerate(arrs):
    plt.figure(figsize=(4, 3))
    for i,val in enumerate(arr):        
        plt.plot(N,val,label = names[i], marker=markers[i])
    plt.ylabel(plot_names[j])
    plt.xlabel("N")
    plt.grid(1)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(plot_names[j].replace(' ','') + ".eps")

plt.show()

    # layouts.append(dict(title = plot_names[j],
    #           yaxis = dict(title = plot_names[j]),
    #           xaxis = dict(title = "N")))

    # fig = dict(data =traces[j],layout = layouts[j])
    # plotly.offline.plot(fig, auto_open=True,filename=plot_names[j])
