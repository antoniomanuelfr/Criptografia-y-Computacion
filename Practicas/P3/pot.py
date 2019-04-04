import numpy 
import practica1
from random import randint

def find_gen(n,p):
    l = []
    ret = True
    for i in range (2,n-1):
        for a in p:
            prob = practica1.potencia_modular(i,(n-1)//a,n)
            if prob == 1:
                ret = False
        if ret :
            l.append(i)
            
    return l


"""
Calcular generadores de Z_n cutre mode 
"""
def potencias(a,n):
    lista = [1]
    res = a

    while res!= 1:
        lista.append(res)
        res = (res*a)%n
    return lista

if __name__ == "__main__":
    
    b=1
    l=[]
    n = practica1.primo_fuerte(10000)
    print (n)
    for i in range (1,n-1):
        b = practica1.potencia_modular(i,(n-1)//2,n)
        if b !=1:
            l.append(i)
    print (l)