import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot') # select the ggplot style
from matplotlib.backends.backend_pdf import PdfPages


pdf = PdfPages('graphs.pdf') # Open a file to write different graphs to; don't forget to close the PDF later!
def line_plot(df, title, xlabel, ylabel, pdf=None):
    fig = df.plot.line(title=title, marker='s', figsize=(10,7))
    # use the line below instead on older versions if the margins are off
    # fig = df.plot.line(title=title, x=df.index, marker='s', figsize=(10,7)) 
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if pdf != None:
        pdf.savefig()
    return fig

# convenience function to create bar plots in a single line, with some convenient default values    
def bar_plot(df, title, xlabel, ylabel, pdf=None):
    fig = df.plot.bar(title=title, figsize=(10,7))
    # use the line below instead on older versions if the margins are off
    # fig = df.plot.line(title=title, x=df.index, figsize=(10,7)) 
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if pdf != None:
        pdf.savefig(fig)
    return fig


# In[ ]:


line_plot(sendrate_df, "Send rate with varying link load".format(load_value), 'Link load', 'Send rate [flits/time unit]', pdf)

line_plot(latency_df, "Latency with varying link load".format(load_value), 'Link load', 'Latency [time unit]', pdf)



latency12_df = latency_df[['Latency1', 'Latency2']] # select only the Latency1 and Latency2 columns
line_plot(latency12_df, "Link load for Node 1 and 2", 'Link load', 'Latency [time units]', pdf)

if pdf != None:
    pdf.close()
pdf = None # remove the reference to the multipage PDF




pdf = PdfPages('graphs.pdf') # Open a file to write different graphs to; don't forget to close the PDF later!
def line_plot(df, title, xlabel, ylabel, pdf=None):
    fig = df.plot.line(title=title, marker='s', figsize=(10,7))
    # use the line below instead on older versions if the margins are off
    # fig = df.plot.line(title=title, x=df.index, marker='s', figsize=(10,7)) 
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if pdf != None:
        pdf.savefig()
    return fig

