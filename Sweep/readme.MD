# How to use

Make sure you have Jupyter installed (via Anaconda, Miniconda, or pip). See http://conda.pydata.org/docs/get-started.html for more information.

Extract all files to a folder of your choice (e.g. D:/multiprocessors/python_sweep/)

From a command line, run the following command:

 jupyter notebook --notebook-dir=<path_to_notebook>
 
for the example directory given above, the full command is: 

 jupyter notebook --notebook-dir=D:/multiprocessors/python_sweep/

After some time, a new browser window will appear. Open the `bus.ipynb` notebook, and select <Cell->Run All> to run the experiment and generate the output graphs.

Check the documentation on http://jupyter-notebook.readthedocs.io/en/latest/examples/Notebook/Running%20Code.html for an introduction of how to use Jupyter notebooks.

# Rotalumis Runner

The Rotalumis runner is used to run POOSL models. It is used in the `run_network_model.py` module, which creates system instances by replacing parameters.

The replacement occurs on a text-basis. The template contains references to e.g. {params[numberOfNodes]} which are replaced in the script by the actual value.

The files `bus_template.poosl` and `bus.ipynb` show an example of how this mechanism can be used to automate experiments.