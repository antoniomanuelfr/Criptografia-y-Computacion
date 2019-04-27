# -*- coding: utf-8 -*-
import numpy as np
import util

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
    if not util.primality.is_prime(p):
        return None
    
    if a < 2 or a > p-2:
        return None

    if b < 1 or b > p-1:
        return None
    
    for i in range (0,p-1):
        res = util.math.power_optimize(a,i,p)
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

    s = util.math.square(p) + 1
    tabla1 = [b]
    for i in range (1,s):
        exp = util.math.power_optimize(a,i,p)
        tabla1.append((b*exp)%p)
