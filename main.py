#!/usr/bin/python3
import qcircuits as qc
import numpy as np
import library as lib

L = {0b001,0b010,0b011,0b101,0b100,0b110,0b101,0b111}
while(len(L) != 1):
    phi = lib.SimonEM()
    v = phi.to_column_vector()
    S = lib.SetOfSol(v)
    if(S != L):
        L = L&S
    else:
        continue
print("the key is k = ",L)
