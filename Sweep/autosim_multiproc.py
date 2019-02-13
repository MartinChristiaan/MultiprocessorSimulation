import pandas as pd
#from bus import simulate
import numpy as np
import time
import sys

from multiprocessing import Process,Queue


# if __name__ == '__main__':
#     p = Process(target=f, args=('bob',))
#     p.start()
#     p.join()



def perform_sim(q,rq,simfun,dim_names,id):
    while q.qsize()>0:
        row = list(q.get())
        row.append(id)
        names,vals = simfun(*tuple(row))
        colnames = names
        colnames.extend(dim_names)
        newrow = vals
        newrow.extend(row[:-1])
        row_df = pd.DataFrame([newrow],columns = colnames)
        rq.put(row_df)
    return
    

def autosim_multiproc(simfun,config_df,resultpath="result.csv"):

    result_df = pd.DataFrame()
    names = []
    newcols = []
    dt = 0
    rq = Queue()
    q = Queue()

    for i,row in config_df.iterrows():
        q.put(row)

    processes = []
    for i in range(1,4):
       p = Process(target=perform_sim, args=(q,rq,simfun,config_df.columns,i))
       p.start()
       processes.append(p)
 
    while q.qsize()>0:
        tstart = time.time()
        row = list(q.get())
        row.append(0)
        itemsleft = q.qsize()
        str_1 = "Now simulating : "
        for j,cname in enumerate(config_df.columns):
            str_1 += " " + cname + " : " + str(row[j])

        mystr = "items left : " + str(itemsleft)+ " ,time last sim :  {:.2f}".format(dt) + " sec ,est time rem : " + str(itemsleft * dt) + " sec"  
        
        print(str_1)
        print(mystr)
        names,vals = simfun(*tuple(row))
        colnames = names
        colnames.extend(config_df.columns)
        
        newrow = vals
        newrow.extend(row[:-1])
        row_df = pd.DataFrame([newrow],columns = colnames)
        result_df = result_df.append(row_df)
        # except Exception as e:
        #     print("There was a failure for " + str_1)
        #     print(e)
        dt = time.time()-tstart
    
    for p in processes:
       p.join()
    while rq.qsize()>0:
        print("Grabbing Results")
        result_df = result_df.append(rq.get())

    if resultpath!=None:
        result_df.to_csv("result.csv",index = False)
    return result_df
  






