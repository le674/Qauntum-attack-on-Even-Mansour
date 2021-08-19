#!/usr/bin/python3
import qcircuits as qc
import numpy as np
import library as lib
import sys
import time

s = []
for i in range(0,15):
    phi = lib.SimonEM()
    v = phi.to_column_vector()
    x = lib.QubitToVector(v)
    while(len(x) < 12):
        x = x[:2] + '0' + x[2:]
    s.append([int(d) for d in x[2:]])
M = np.array(s,dtype=object)
B = lib.gauss(M)
C = lib.gaussH(B)
N  = lib.ReduceM(C)
if(len(N) < 9):
    print("pas de solution")
    sys.exit(False)
else:
    k = lib.solver(N)
    print(k)
    sys.exit(True)
