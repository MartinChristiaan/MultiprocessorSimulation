
import run_network_model
import os, numpy
import pandas

## Params
nrNodes = 4
output_directory_template = 'Bus4/load_{0}'
model_path = 'C:\\Users\\marti\\source\\repos\\Multiprocessing\\POOSL_IDE'
soc_type = 'Bus_4_nodes'
load_values = [0.1,0.2,0.3,0.4] # 10 evenly spaced values between 0.05 and 0.95

def simulate(load_value,NIBufferCapacity,SoC_type,nrNodes):
    print("Running experiment for load = {0}".format(load_value))
    output_directory = os.path.abspath(output_directory_template.format(load_value))
    model_parameters = {'Load' : load_value, 
                        'NIBufferCapacity' : NIBufferCapacity,
                        'SoC_type' :  SoC_type,
                        'NumberOfNodes' : nrNodes
                        }
    if run_network_model.run_network_model(
            [model_path], # library paths
            open('bus_template.poosl').read(), # system instance template
        nrNodes, model_parameters, output_directory) == False:
        raise Exception("Model did not terminate to completion, check the output of Rotalumis!")
        output_directory = os.path.abspath(output_directory_template.format(load_value))

    for i in range(1, nrNodes + 1):
        latency_log = "Latency{0}".format(i)
        sendrate_log = "Sendrate{0}".format(i)
        latency_df.loc[load_value].at[latency_log] = readLog(os.path.join(output_directory, latency_log) + ".log")
        sendrate_df.loc[load_value].at[sendrate_log] = readLog(os.path.join(output_directory, sendrate_log) + ".log")
    
    return names,load_values



def readLog(fname):
    if not os.path.exists(fname):
        raise Exception("Unable to read log: \"{0}\" does not exist!".format(fname))
        
    with open(fname) as log_file:
        for line in log_file:
            parts = line.split('\t')
            try:
                value = float(parts[0].strip())
            except ValueError:
                pass
        return value

sendrate_columns = {}
latency_columns = {}
for i in range(1, nrNodes + 1):
    sendrate_columns["Sendrate" + str(i)] = [float('NaN')] # data is not yet set
    latency_columns["Latency" + str(i)] = [float('NaN')] # data is not yet set

sendrate_df = pandas.DataFrame(data=sendrate_columns)
latency_df = pandas.DataFrame(data=latency_columns)

for load_value in load_values:

latency_df['average'] = latency_df.mean(axis=1) 
sendrate_df['average'] = sendrate_df.mean(axis=1) 






latency_df.to_csv('Latency.csv') # load back into dataframe by using: df = pandas.from_csv('Latency.txt')
sendrate_df.to_csv('Sendrate.csv')

