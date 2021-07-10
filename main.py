#!/usr/bin/python3
import qcircuits as qc
import numpy as np
import library as lib

phi = lib.SimonEM()
v = phi.to_column_vector()
K = lib.KeyRecovery(v)
print("the possible keys are k0 = ",K[0],", k1 = ",K[1],"k = ",K[2])
