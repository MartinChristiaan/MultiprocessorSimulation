import pandas as pd
from bus import simulate
import numpy as np
df = pd.read_csv("config.csv")

dims = []
datas = []

combi_data = []
for column in df:
    col_data = df[column].values
    dims.append(len(col_data))
    datas.append(col_data)

for i,dim in enumerate(dims):
    combi_data.append([])

    post_i_mul =1    
    if i < len(dims)-1:
        post_i_mul =int(np.prod(dims[i+1:]))

    pre_i_mul = 1
    if i > 0:
        pre_i_mul = int(np.prod(dims[:i]),1)

    for pre in range(pre_i_mul):
        for data in datas[i]:
            for z in range(post_i_mul):
                combi_data[i].append(data)
combi_df = pd.DataFrame()
for i,column in enumerate(df):
    combi_df[column] = combi_data[i]
combi_df.to_csv("combi.csv")





