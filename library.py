#!/usr/bin/python3
import qcircuits as qc
import numpy as np
import sys


def Circuits(x):
    CNOT = qc.CNOT()
    X = qc.PauliX()
    toffoli = qc.operators.Toffoli()
    x = CNOT(x,qubit_indices = [0,3])
    x = CNOT(x,qubit_indices = [1,4])
    x = CNOT(x,qubit_indices = [2,5])
    x = toffoli(x,qubit_indices = [3,4,5])
    x = X(x,qubit_indices = [4])
    x = toffoli(x,qubit_indices = [5,4,3])
    x = CNOT(x,qubit_indices = [0,6])
    x = CNOT(x,qubit_indices = [1,7])
    x = CNOT(x,qubit_indices = [2,8])
    x = X(x,qubit_indices = [7])
    x = X(x,qubit_indices = [8])
    x = toffoli(x,qubit_indices = [6,7,8])
    x = X(x,qubit_indices = [7])
    x = toffoli(x,qubit_indices = [8,7,6])
    x = CNOT(x,qubit_indices = [3,6])
    x = CNOT(x,qubit_indices = [4,7])
    x = CNOT(x,qubit_indices = [5,8])
    x = X(x,qubit_indices = [6])
    x = X(x,qubit_indices = [7])
    x = X(x,qubit_indices = [8])
    return x

def SimonEM():
    X = qc.PauliX()
    CNOT = qc.CNOT()
    toffoli = qc.operators.Toffoli()
    H3 = qc.operators.Hadamard(d = 3)
    phi = qc.positive_superposition(d = 3)
    ksi = qc.zeros(6)
    Phi = phi*ksi
    Phi = Circuits(Phi)
    Phi.measure(qubit_indices = [6,7,8], remove = True)
    Phi = toffoli(Phi,qubit_indices = [5,4,3])
    Phi = X(Phi,qubit_indices = [4])
    Phi = toffoli(Phi,qubit_indices = [3,4,5])
    Phi = CNOT(Phi,qubit_indices = [0,3])
    Phi = CNOT(Phi,qubit_indices = [1,4])
    Phi = CNOT(Phi,qubit_indices = [2,5])
    Phi.measure(qubit_indices = [3,4,5],remove = True)
    Phi = H3(Phi,qubit_indices = [0,1,2])
    Phi.measure(qubit_indices = [0,1,2],remove = False)
    return Phi

def  SetOfSol(v):
    for t in range(0,len(v)):
        if((v[t] == 1) or (v[t] == -1)):
            indice = t
            break
        else:
            pass
    x = bin(t)
    if(int(x,2) == 0):
        return {0b001,0b010,0b011,0b101,0b100,0b001,0b101,0b111}
    elif(int(x,2) == 1):
        return {0b001,0b010,0b011}
    elif(int(x,2) == 2):
        return {0b101,0b100,0b001}
    elif(int(x,2) == 3):
        return {0b011,0b100,0b111}
    elif(int(x,2) == 4):
        return {0b001,0b010,0b011}
    elif(int(x,2) == 5):
        return {0b010,0b101,0b111}
    elif(int(x,2) == 6):
        return {0b110,0b111,0b001}
    else:
        return {0b011,0b101,0b110}
