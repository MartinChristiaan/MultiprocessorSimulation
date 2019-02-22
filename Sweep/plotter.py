import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
matplotlib.style.use('ggplot')
def get_dims(nplots):
    if nplots == 1 : return 1,1
    if nplots == 2 : return 1,2
    if nplots == 3 : return 1,3
    if nplots == 4 : return 2,2
    if nplots == 5 : return 1,5
    if nplots == 6 : return 2,3
    if nplots == 7 : return 1,7
    if nplots == 8 : return 2,4
    if nplots == 9 : return 3,3

df = pd.read_csv("results_ringtorus.csv")


filter_vals = [("NIBufferCapacity",2),("Interconnect","Torus")]


x_dim = "NumberOfNodes"
y_dims = [["Latency Average", "Latency Min","Latency Max"],["Sendrate Average",  "Sendrate Min"  ,"Sendrate Max"]] 
trace_dim = "Load Value"
# color_dim = "Load Value"
# symbol_dim = "Load Value"
# annotation_dim = "Load Value"

for fval in filter_vals:
    df = df[df[fval[0]] == fval[1]]

df = df.sort_values(x_dim)
markers = ["o","v","^","<",">","1","2","3","4"]

nplots = len(y_dims)
dimx,dimy = get_dims(nplots)
plt.figure()    
for i in range(nplots):
    plt.subplot(dimy,dimx,i+1)
    traces = df[trace_dim].unique()
    traces.sort()
    mylines = []
    for k,trace in enumerate(traces):
        trace_df = df[df[trace_dim] == trace]
        y_min = trace_df[y_dims[i][1]]
        y_max = trace_df[y_dims[i][2]]
        x = trace_df[x_dim]
        y = trace_df[y_dims[i][0]]
        plt.plot(x,y,label = trace_dim.split()[0] + " : " +  str(trace),marker = markers[k])
        plt.fill_between(x,y_min,y_max, alpha=0.3)
        line_end = x.values[-1], y.values[-1]
        # plt.annotate('local max', xy=line_end,  xycoords='data',
        #     xytext=line_end,horizontalalignment='right', verticalalignment='top'
        #     )
    plt.legend()
    plt.xlabel(x_dim)
    plt.ylabel(y_dims[i][0].split()[0])
    plt.grid(1)

plt.show()
















