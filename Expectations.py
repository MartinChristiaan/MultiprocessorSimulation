import numpy as np


import plotly
import plotly.graph_objs as go
from plotly import tools


names = ["Bus","Mesh","Torus","Tree"]
plot_names = ["latency","Bisecion Bandwidth","Number of Links","Number of Routers"]
N = np.arange(0,33)

latencies = [np.ones_like(N),2*np.sqrt(N)/3,np.sqrt(N)/2,2*np.log2(N)]
bisection_bandwidths = [np.ones_like(N),np.sqrt(N),2*np.sqrt(N),N*2]
num_links = [N,(np.sqrt(N)-1)*2*np.sqrt(N),2*N,np.log2(N)*N*2]
num_routers = [np.ones_like(N),N,N,N-1]


arrs = [latencies,bisection_bandwidths,num_links,num_routers]

traces = [[],[],[],[]]
layouts = []
for j,arr in enumerate(arrs):
    for i,val in enumerate(arr):
        traces[j].append(go.Scatter(
            x = N,
            y = val,
            mode = 'lines',
            name = names[i]
        ))
    layouts.append(dict(title = plot_names[j],
              yaxis = dict(title = plot_names[j]),
              xaxis = dict(title = "N")))

    fig = dict(data =traces[j],layout = layouts[j])
    plotly.offline.plot(fig, auto_open=True,filename=plot_names[j])
