#!/usr/bin/python3
import qcircuits as qc
import numpy as np
import sys
def Circuits(x):
    CNOT = qc.CNOT()
    X = qc.PauliX()
    toffoli = qc.operators.Toffoli()
    #----------------------------------------------------
    #First copy
    for i in range(0,10):
        x = CNOT(x,qubit_indices = [i,i+10])

    #------------------------------------------------------
    #Adding the key
    x = X(x,qubit_indices = [10])
    x = X(x,qubit_indices = [13])
    x = X(x,qubit_indices = [19])
    #-----------------------------------------------------
    #Permutation over the first register
    x = toffoli(x,qubit_indices = [0,1,2])
    x = toffoli(x,qubit_indices = [1,2,3])
    x = toffoli(x,qubit_indices = [2,3,4])
    x = toffoli(x,qubit_indices = [3,4,5])
    x = toffoli(x,qubit_indices = [4,5,6])
    x = toffoli(x,qubit_indices = [5,6,7])
    x = toffoli(x,qubit_indices = [6,7,8])
    x = toffoli(x,qubit_indices = [8,9,0])
    x = toffoli(x,qubit_indices = [9,0,1])
    #-----------------------------------------------------
    #Permutation over the second register
    x = toffoli(x,qubit_indices = [10,11,12])
    x = toffoli(x,qubit_indices = [11,12,13])
    x = toffoli(x,qubit_indices = [12,13,14])
    x = toffoli(x,qubit_indices = [13,14,15])
    x = toffoli(x,qubit_indices = [14,15,16])
    x = toffoli(x,qubit_indices = [15,16,17])
    x = toffoli(x,qubit_indices = [16,17,18])
    x = toffoli(x,qubit_indices = [18,19,10])
    x = toffoli(x,qubit_indices = [19,10,11])
    #-----------------------------------------------------
    #Compute P(x) xor P(x xor k)
    for i in range(0,10):
        x = CNOT(x,qubit_indices = [i,i + 10])
    #------------------------------------------------------
    #Adding the second key
    x = X(x,qubit_indices = [10])
    x = X(x,qubit_indices = [16])
    x = X(x,qubit_indices = [17])
    x = X(x,qubit_indices = [19])
    #------------------------------------------------------
    return x

def SimonEM():
    X = qc.PauliX()
    CNOT = qc.CNOT()
    toffoli = qc.operators.Toffoli()
    H10 = qc.operators.Hadamard(d = 10)
    phi = qc.positive_superposition(d = 10)
    ksi = qc.zeros(10)
    Phi = phi*ksi
    Phi = Circuits(Phi)
    #We apply the inverse of the Permutation
    #--------------------------------------------------------
    Phi = toffoli(Phi,qubit_indices = [9,0,1])
    Phi = toffoli(Phi,qubit_indices = [8,9,0])
    Phi = toffoli(Phi,qubit_indices = [6,7,8])
    Phi = toffoli(Phi,qubit_indices = [5,6,7])
    Phi = toffoli(Phi,qubit_indices = [4,5,6])
    Phi = toffoli(Phi,qubit_indices = [3,4,5])
    Phi = toffoli(Phi,qubit_indices = [2,3,4])
    Phi = toffoli(Phi,qubit_indices = [1,2,3])
    Phi = toffoli(Phi,qubit_indices = [0,1,2])
    #--------------------------------------------------------
    #We measure the last register
    Phi.measure(qubit_indices = [10,11,12,13,14,15,16,17,18,19],remove = True)
    #On applique la transformé de Hadamard sur les premier registres
    Phi = H10(Phi,qubit_indices = [0,1,2,3,4,5,6,7,8,9])
    #--------------------------------------------------------
    #We measure the first register
    Phi.measure(qubit_indices = [0,1,2,3,4,5,6,7,8,9],remove = False)
    return Phi


def  QubitToVector(v):
    for t in range(0,len(v)):
        if((v[t] == 1) or (v[t] == -1)):
            indice = t
            break
        else:
            pass
    x = bin(t)
    return x

def ReduceM(M):
    Index = []
    count = 0
    for i in range(0,len(M)):
        count = 0
        for j in range(0,10):
            if(M[i,j] == 1):
                count += 1
        if(count == 0):
            Index.append(i)
    for i in range(len(Index) - 1,-1,-1):
        M = np.delete(M,(Index[i]), axis =0)
    return M

def pivot_index(M,i):
    n = len(M)
    j = i
    for k in range(i + 1,n):
        if(M[k,i] > M[i,i]):
            j = k
            return j
    return i

def pivot_indexH(M,i):
    j = i
    for k in range(i,0,-1):
        if(M[k,i] > M[i,i]):
            j = k
            return j
    return i

def swapline(M,i,j):
    for k in range(0,10):
        tmp = M[i,k]
        M[i,k] = M[j,k]
        M[j,k] = tmp

def transvection_lines(M,i,k,factor):
    for j in range(0,10):
        M[k,j] = (M[k,j] + M[i,j]*factor)%2

def gauss(M):
    for i in range(0,10):
        ipiv =  pivot_index(M,i)
        if(ipiv != i):
            swapline(M,i,ipiv)
        for k in range(i + 1,len(M)):
            factor = M[k,i]
            transvection_lines(M,i,k,factor)
    return M

def gaussH(M):
    for i in range(9,1,-1):
        ipiv = pivot_indexH(M,i)
        if(ipiv != i):
            swapline(M,i,ipiv)
        for k in range(i - 1,0,-1):
            factor = M[k,i]
            transvection_lines(M,i,k,factor)
    return M

def solver(M):
    for i in range(1,1024):
        tmp = bin(i)[2:]
        l = [int(i) for i in tmp]
        while(len(l) != 10):
            l = [0] + l
        arr = np.array(l)
        hyp = M.dot(arr)
        if(all(x%2 == 0 for x in hyp)):
            return arr
