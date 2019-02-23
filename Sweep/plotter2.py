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

df = pd.read_csv("results/results_combined.csv")
filter_vals = [("NIBufferCapacity",2)]
anti_filter = [("Load Value",0.15)]
x_dim = "NumberOfNodes"
y_dims = ["Latency Average","Sendrate Average"]
 
trace_dim = "Interconnect"
plot_dim = "Load Value"
# color_dim = "Load Value"
# symbol_dim = "Load Value"
# annotation_dim = "Load Value"

for fval in filter_vals:
    df = df[df[fval[0]] == fval[1]]
for fval in anti_filter:
    df = df[df[fval[0]] != fval[1]]

df = df.sort_values(x_dim)
markers = ["o","v","^","<",">","1","2","3","4"]

for y_dim in y_dims:
    plt.figure()    
    plots = df[plot_dim].unique()
    plots.sort()
    nplots = len(plots)
    dimx,dimy = get_dims(nplots)

    for i,plotd in enumerate(plots):
        ax = plt.subplot(dimy,dimx,i+1)
        ax.set_title("load : " + str(plotd))
        plot_df = df[df[plot_dim] == plotd]
        traces = plot_df[trace_dim].unique()
        traces.sort()
        mylines = []
        for k,trace in enumerate(traces):
            trace_df = plot_df[plot_df[trace_dim] == trace]
            x = trace_df[x_dim]
            y = trace_df[y_dim]
            plt.plot(x,y,label = str(trace),marker = markers[k])
            
            line_end = x.values[-1], y.values[-1]
            # plt.annotate('local max', xy=line_end,  xycoords='data',
            #     xytext=line_end,horizontalalignment='right', verticalalignment='top'
            #     )
        plt.legend()
        plt.xlabel(x_dim)
        plt.ylabel(y_dim.split())
        plt.grid(1)

plt.show()
















