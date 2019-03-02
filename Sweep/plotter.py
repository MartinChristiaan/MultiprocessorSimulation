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


def filter_df(df, eq_filter = [],neq_filter = []):
    for fval in eq_filter:
        df = df[df[fval[0]] == fval[1]]
    for fval in neq_filter:
        df = df[df[fval[0]] != fval[1]]
    return df
    



def create_figure(figtype = "paper"):
    if figtype == "paper":
        plt.figure(figsize=(3.5,2.5))    
   
    
def seperate_dim(df,dim):
    sep_id = df[dim].unique()
    sep_id.sort()
    sep = [df[df[dim] == i] for i in sep_id]
 
    return sep,sep_id

#def create_subplotfigure(figtype = "paper")
    # if subplot_dim != None:
    #     plots = df[d.subplot_dim].unique()
    #     plots.sort()
    #     nplots = len(plots)
    #     dimx,dimy = get_dims(nplots)
    #     plt.figure(figsize=(dimx*3.5,dimy*2.5))    
 


def plot_traces(df,x_dim,y_dim,trace_dim,trace_label_fun = None, title_fun = None,annotate = False):
    df = df.sort_values(x_dim)
    markers = ["o","v","^","<",">","1","2","3","4"]
    
#     for i,plotd in enumerate(plots):
#         ax = plt.subplot(dimy,dimx,i+1)
#         plt_title = str(plotd)
#         if not title_fun == None:
#             plt_title = title_fun(plotd)
#         ax.set_title(plt_title)
#         plot_df = df[df[d.plot_dim] == plotd]
#         traces = plot_df[d.trace_dim].unique()
#         traces.sort()
# #            mylines = []
    
    traces,trace_values = seperate_dim(df,trace_dim)
    for k,trace in enumerate(trace_values):
        trace_df = traces[k]
        x = trace_df[x_dim]
        y = trace_df[y_dim]
        mylabel = str(trace)
        if trace_label_fun!=None:
            mylabel = trace_label_fun(trace)
        plt.plot(x,y,label = mylabel,marker = markers[k])
        if annotate:
            line_end = x.values[-1], y.values[-1]
            plt.annotate(mylabel, xy=line_end,  xycoords='data',
                xytext=line_end,horizontalalignment='right', verticalalignment='top'
                )
    plt.legend()
    plt.xlabel(x_dim)
    plt.ylabel(y_dim)
    plt.grid(1)
    plt.tight_layout()
    return plt













