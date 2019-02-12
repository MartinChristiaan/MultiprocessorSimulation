
import run_network_model
import os, numpy
import pandas as pd
from autosim import autosim,get_all_combinations


# def generate_model(nrNodes):
#     instancesfile = open("demofile.txt")
#     basednetworkfile = open("")
#     node_declrs = []
#     channel_declrs = []
#     ports =[]
#     interface_instances = []
#     arbiter_channels = []
#     bus_channels = []
#     interface_channels = []
#     for node in range(nrNodes):
#         node_declr = "N" + str(node) + ": Node(AccuracyCheckInterval := AccuracyCheckInterval, LinkCapacity := LinkCapacity, Load := Load, MeanBurstSize := MeanBurstSize, MyID := 1, NumberOfNodes := NumberOfNodes)"
#         node_declrs.append(node_declr)
#         channel_declr = "{N"+str(node) +".NI, Network.Node"+str(node) + " }"
#         channel_declrs.append(channel_declr) 

        





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


def simulate(nrNodes,load_value,NIBufferCapacity,SoC_type):
    output_directory_template = 'Bus4/load_{0}'
    model_path = 'C:\\Users\\marti\\source\\repos\\Multiprocessing\\POOSL_IDE'

    nrNodes = int(nrNodes)
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

    latency_names = []
    sendrate_names = []
    latency_values = []
    sendrate_values = []
    for i in range(1, nrNodes + 1):
        latency_names+=[("Latency{0}".format(i))]
        sendrate_names+=[("Sendrate{0}".format(i))]

        latency_values += [readLog(os.path.join(output_directory, latency_names[i-1]) + ".log")]
        sendrate_values += [readLog(os.path.join(output_directory, sendrate_names[i-1]) + ".log")]
    
    return latency_names+sendrate_names,latency_values + sendrate_values


config_df = pd.read_csv("config.csv")
combi_config = get_all_combinations(config_df)
autosim(simulate,combi_config)





