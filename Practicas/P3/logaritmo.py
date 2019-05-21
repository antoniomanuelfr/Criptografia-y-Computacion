# -*- coding: utf-8 -*-
import numpy as np
import util.math as mt
import util.primality as pr
import matplotlib.pyplot as plt
import random
from time import time

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
    actual = b
    tabla1 = [actual]

    for i in range (1,s):
        actual = (actual * a )%p
        tabla1.append(actual)

    f1 = (a**s)%p
    t = 1 
    f = f1
    while t*s < s**2:
        if f in tabla1: 
            return ((t*s) - tabla1.index(f)) % p        
        f = (f*f1)%p
        t+=1

    return None
def pseudo(a,b,p,sec):
    """
    brief
    -------------
        Genera el siguiente elemento de una secuencia aleatoria de la siguiente forma:\n
        (x_i+1, alpha_i+1, beta_i+1) de la siguiente forma: 

        si xi mod 3 == 1: x_i+1 = x_i*b mod p, alpha_i+1=aplha_i, beta_i+1= beta_i +1
        si xi mod 3 == 0: x_i+1 = x_i^2 mod p, alpha_i+1=2*aplha_i mod p-1, beta_i+1= 2beta_i mod p-1
        si xi mod 3 == 2: x_i+1 = x_i*a mod p, alpha_i+1= aplha_i +1, beta_i+1=beta_i

        

    Parameter
    ------------

        a : Base del logaritmo\n
        b : Antilogaritmo\n
        p : Modulo\n
        sec: Lista con los parametros (por orden de aparicion) x, alpha y beta de la sucesion.

    Result
    ------------

        (x_i+1, alpha_i+1, beta_i+1) 
    """
    if len(sec)!=3: 
        return None

    x_i = sec[0]
    alpha_i = sec[1]
    beta_i = sec[2]
    
    if x_i % 3 == 1: 
        x_next = (x_i*b)%p
        alpha_next = alpha_i
        beta_next = beta_i+1

    elif  x_i % 3 == 0:
        x_next = (x_i*x_i)%p
        alpha_next = (2*alpha_i) % (p-1)
        beta_next = (2*beta_i) % (p-1)
    
    else:
        x_next = (x_i*a)%p
        alpha_next = alpha_i+1
        beta_next = beta_i

    return [x_next,alpha_next, beta_next]

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
    # Calculamos x_n
    sec_1 =  pseudo(a,b,p,[1,0,0])
    # Calculamos x_{2n}
    sec_2 =  pseudo(a,b,p,sec_1)

    while (sec_1[0]!=sec_2[0]):
        # Siguientes pasos de la secuencia
        sec_2 = pseudo(a,b,p,pseudo(a,b,p,sec_2))
        sec_1 = pseudo(a,b,p,sec_1)

    # Resolvemos la congruencia 
    return mt.congruencia(sec_2[2]-sec_1[2],sec_1[1]-sec_2[1],p-1)

if __name__ == '__main__':
    sel = int(input("Introduzca:\n1. para usar fuerza bruta.\n2. para paso enano - paso gigante.\n3. para Rho de Pollard\n"))
    if sel == 1: 
        n_iters = 12 # 12
        title = "Fuerza Bruta"
    elif sel == 2: 
        n_iters = 16 # 16
        title = "Paso enano - Paso gigante"
    else: 
        n_iters = 26 #26
        title = "Rho de Pollard"

    primos = []
    tiempos = []
    bits = 5
    paso = 2
    p_n = pr.next_prime_strong(2**bits)
    for i in range (n_iters):
        time_1 = time()
        
        if sel != 2: 
            a = random.randint(2,p_n-2)
        else: 
            a = (p_n-1)//2

        res = log_bf(10,a,p_n)
        time_2 = time()

        primos.append(p_n)
        tiempos.append(time_2-time_1)

        bits+=paso
        print("Iteracion {} usando un primo con {} bits en {} segundos".format(i,bits,time_2-time_1))

        p_n = pr.next_prime_strong(2**bits)

    plt.xlabel('Primo')
    plt.ylabel('Tiempo en segundos')
    plt.title(title)
    plt.plot(primos,tiempos)
    plt.show()