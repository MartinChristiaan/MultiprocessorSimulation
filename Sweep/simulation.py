
import run_network_model
import os
import numpy as np
import pandas as pd
from autosim import autosim,get_all_combinations
from autosim_multiproc import autosim_multiproc
import copypastahero
from math import sqrt
def readLog(fname):
    if not os.path.exists(fname):
        raise Exception("Unable to read log: \"{0}\" does not exist!".format(fname))
        
    with open(fname) as log_file:
        value = np.nan
        for line in log_file:
            parts = line.split('\t')
            try:
                value = float(parts[0].strip())
            except ValueError:
                pass
        return value


def parse_results(nrNodes,output_directory):
    
    latency_names = ["Latency Average","Latency Min","Latency Max"]
    sendrate_names = ["Sendrate Average","Sendrate Min","Sendrate Max"]
    latency = []
    sendrate = []
    for i in range(1, nrNodes + 1):
        latency += [readLog(os.path.join(output_directory, "latency"+str(i)) + ".log")]
        sendrate += [readLog(os.path.join(output_directory, "sendrate"+str(i)) + ".log")]
    
    
    
    return latency_names+sendrate_names,[np.mean(latency),np.min(latency),np.max(latency),np.mean(sendrate),np.min(sendrate),np.max(sendrate)]



def simulate_bus(nrNodes,load_value,NIBufferCapacity,myid=0):
    output_directory_template = 'Bus4/nrNodes_' + str(nrNodes) + "_load_" + str(load_value) + "_bufcap_" + str(NIBufferCapacity)
    model_path = os.getcwd()+'\\poosl_model'+str(myid)
    instances_path = model_path + "\\bus\\instances.poosl"
    network_path = model_path + "\\bus\\BusBasedNetwork.poosl"
    nrNodes = int(nrNodes)
    
    # Generate code for n nodes
    copypastahero.cook_copypasta('sourcefiles\\BasedNetworkSource.poosl',network_path,nrNodes)
    copypastahero.cook_copypasta('sourcefiles\\instancesSource.poosl',instances_path,nrNodes)    

    output_directory = os.path.abspath(output_directory_template)
    model_parameters = {'Load' : load_value, 
                        'NIBufferCapacity' : int(NIBufferCapacity),
                        'SoC_type' :  "Bus_N_nodes",
                        'NumberOfNodes' : nrNodes
                        }
    if run_network_model.run_network_model(
        [model_path], # library paths
        open('sourcefiles\\bus_template.poosl').read(), # system instance template
        nrNodes, model_parameters, output_directory) == False:
            raise Exception("Model did not terminate to completion, check the output of Rotalumis!")
    
    output_directory = os.path.abspath(output_directory_template.format(load_value))
    return parse_results(nrNodes,output_directory)

def get_dims(nrNodes):
    if nrNodes == 4: return 2,2
    if nrNodes == 6: return 3,2
    if nrNodes == 8: return 4,2
    if nrNodes == 9: return 3,3
    if nrNodes == 12: return 4,3
    if nrNodes == 16: return 4,4
    if nrNodes == 20: return 5,4
    if nrNodes == 25: return 5,5
    raise ValueError('Nr Nodes not allowed')

def simulate_mesh(nrNodes,load_value,NIBufferCapacity,myid=0):
    output_directory_template = 'mesh/nrNodes_' + str(nrNodes) + "_load_" + str(load_value) + "_bufcap_" + str(NIBufferCapacity)
    model_path = os.getcwd()+'\\poosl_model'+str(myid)
    instances_path = model_path + "\\mesh\\instances.poosl"
    network_path = model_path + "\\mesh\\MeshBasedNetwork.poosl"
    nrNodes = int(nrNodes)
    dimx,dimy = get_dims(nrNodes)
    #Generate code for n nodes
    copypastahero.cook_copypasta('sourcefiles\\MeshBasedNetwork.poosl',network_path,nrNodes)
    copypastahero.cook_copypasta('sourcefiles\\mesh_instances.poosl',instances_path,nrNodes)    
    copypastahero.cook_mesh(dimx,dimy,model_path + "\\mesh\\Meshnxn.poosl")

    output_directory = os.path.abspath(output_directory_template)
    model_parameters = {'Load' : load_value, 
                        'NIBufferCapacity' : int(NIBufferCapacity),
                        'SoC_type' : 'Mesh_nxn',
                        'NumberOfXNodes' : dimx,
                        'NumberOfYNodes' : dimy
                        }
    if run_network_model.run_network_model(
        [model_path], # library paths
        open('sourcefiles/mesh_template.poosl').read(), # system instance template
        nrNodes, model_parameters, output_directory) == False:
            raise Exception("Model did not terminate to completion, check the output of Rotalumis!")
    
    output_directory = os.path.abspath(output_directory_template.format(load_value))
    return parse_results(nrNodes,output_directory)

def simulate_torus(nrNodes,load_value,NIBufferCapacity,myid=0):
    output_directory_template = 'torus/nrNodes_' + str(nrNodes) + "_load_" + str(load_value) + "_bufcap_" + str(NIBufferCapacity)
    model_path = os.getcwd()+'\\poosl_model'+str(myid)
    instances_path = model_path + "\\torus\\instances.poosl"
    network_path = model_path + "\\torus\\TorusBasedNetwork.poosl"
    nrNodes = int(nrNodes)
    dimx,dimy = get_dims(nrNodes)
    #Generate code for n nodes
    copypastahero.cook_copypasta('sourcefiles\\TorusBasedNetwork.poosl',network_path,nrNodes)
    copypastahero.cook_copypasta('sourcefiles\\torus_instances.poosl',instances_path,nrNodes)    
    copypastahero.cook_torus(dimx,dimy,model_path + "\\torus\\Torusnxn.poosl")

    output_directory = os.path.abspath(output_directory_template)
    model_parameters = {'Load' : load_value, 
                        'NIBufferCapacity' : int(NIBufferCapacity),
                        'SoC_type' : 'Torus_nxn',
                        'NumberOfXNodes' : dimx,
                        'NumberOfYNodes' : dimy
                        }
    if run_network_model.run_network_model(
        [model_path], # library paths
        open('sourcefiles/torus_template.poosl').read(), # system instance template
        nrNodes, model_parameters, output_directory) == False:
            raise Exception("Model did not terminate to completion, check the output of Rotalumis!")
    
    output_directory = os.path.abspath(output_directory_template.format(load_value))
    return parse_results(nrNodes,output_directory)

def simulate_ring(nrNodes,load_value,NIBufferCapacity,myid=0):
    output_directory_template = 'ring/nrNodes_' + str(nrNodes) + "_load_" + str(load_value) + "_bufcap_" + str(NIBufferCapacity)
    model_path = os.getcwd()+'\\poosl_model'+str(myid)
    instances_path = model_path + "\\ring\\instances.poosl"
    network_path = model_path + "\\ring\\RingBasedNetwork.poosl"
    nrNodes = int(nrNodes)
    #Generate code for n nodes
    copypastahero.cook_copypasta('sourcefiles\\RingBasedNetwork.poosl',network_path,nrNodes)
    copypastahero.cook_copypasta('sourcefiles\\ring_instances.poosl',instances_path,nrNodes)    
    copypastahero.cook_ring(nrNodes,model_path + "\\ring\\Ringnxn.poosl")

    output_directory = os.path.abspath(output_directory_template)
    model_parameters = {'Load' : load_value, 
                        'NIBufferCapacity' : int(NIBufferCapacity),
                        'SoC_type' : 'Ring',
                        'NumberOfXNodes' : nrNodes,
                        'NumberOfYNodes' : 1
                        }
    if run_network_model.run_network_model(
        [model_path], # library paths
        open('sourcefiles/ring_template.poosl').read(), # system instance template
        nrNodes, model_parameters, output_directory) == False:
            raise Exception("Model did not terminate to completion, check the output of Rotalumis!")
    
    output_directory = os.path.abspath(output_directory_template.format(load_value))
    return parse_results(nrNodes,output_directory)


def simulate(interconnect,nrNodes,load_value,NIBufferCapacity,myid=0):
    if interconnect == "Bus":
        return simulate_bus(nrNodes,load_value,NIBufferCapacity,myid)
    if interconnect == "Mesh":
        return simulate_mesh(nrNodes,load_value,NIBufferCapacity,myid)
    if interconnect == "Torus":
        return simulate_torus(nrNodes,load_value,NIBufferCapacity,myid)
    if interconnect == "Ring":
        return simulate_ring(nrNodes,load_value,NIBufferCapacity,myid)
        
    

if __name__ == "__main__":
    config_df = pd.read_csv("config.csv")
    combi_config = get_all_combinations(config_df)
    autosim_multiproc(simulate,combi_config,resultpath="results/Mesh/results.csv")





