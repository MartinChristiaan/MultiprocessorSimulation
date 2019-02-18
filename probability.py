import numpy as np
N = 4
paths= np.zeros((N-1)*2)

for i in range(N):
    for j in range(N):
        for k in range(j):
            paths[i+k]+=1
print(paths)