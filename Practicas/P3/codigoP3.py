# -*- coding: utf-8 -*-
import numpy as np
import util.math as mt
import util.primality as pr
"""
Algortimos para la resolución del problema del logaritmo discreto
"""


def log_bf(a,b,p):
    """
    brief
    -------------
    Solucion del problema del logaritmo discreto por fuerza bruta

    Parameter
    ------------

    a : Base del logaritmo\n
    b : Antilogaritmo\n
    p : Modulo  

    Result
    ------------

    pos : log_a (b) mod p 
    """
    if not pr.is_prime(p):
        return None
    
    if a < 2 or a > p-2:
        return None

    if b < 1 or b > p-1:
        return None
    
    for i in range (0,p-1):
        res = mt.power_optimize(a,i,p)
        if res == b: 
            return i
    
    return None

def log_pe_pg(a, b, p):
    """
    brief
    -------------
    Solucion del problema del logaritmo discreto con el algoritmo paso enano paso gigante

    Parameter
    ------------

    a : Base del logaritmo\n
    b : Antilogaritmo\n
    p : Modulo  

    Result
    ------------

    pos : log_a (b) mod p 
    """
    s = mt.square(p) + 1
    end_value = (a**(s**2))

    tabla1 = [b]
    for i in range (1,s):
        exp = mt.power_optimize(a,i,p)
        tabla1.append((b*exp)%p)

    end = False
    f1 = (a**s)%p
    t = 1 
    f = f1

    while not end:
        if f in tabla1: 
            end = True
            res_val =  ((t*s) - tabla1.index(f)) % p 
        elif t == end_value:
            res_val = None
            end = True
       
        f = (f*f1)%p
        t+=1

    return res_val

def log_ro_pollard(a, b, p):
    """
    brief
    -------------
    Solucion del problema del logaritmo discreto con el algoritmo Rho de Pollard

    Parameter
    ------------

    a : Base del logaritmo\n
    b : Antilogaritmo\n
    p : Modulo  

    Result
    ------------

    pos : log_a (b) mod p 
"""

if __name__ == '__main__':
    a = 11
    b = 766
    p = 839
    print ("El log_{} {} mod {} usando fuerza bruta es: {}".format(a,b,p,log_bf(a,b,p)))
    print ("El log_{} {} mod {} usando el algoritmo paso pequeño-paso gigante es: {}".format(a,b,p,log_pe_pg(a,b,p)))
