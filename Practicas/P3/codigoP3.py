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
    cnt = 0
    end = False
    # Primera secuencia
    sec_ant = pseudo(a,b,p,[1,0,0])
    # Lista de la secuencia
    sec = [sec_ant]
    # Lista de x_n para buscar 
    x_n = [sec_ant[0]]

    while not end:
        # Genero el paso siguiente de la secuencia
        nueva = pseudo(a,b,p,sec_ant)
        # Incremento en el contador para solo comparar x_n y x_{2n}
        cnt +=1
        if cnt == 2:
            cnt = 0 
            # Comparo si el nuevo x_i esta en la lista de x_anteriores
            if  nueva[0] in x_n: 
                # Si esta devuelvo el el elemento de la secuencia correspondiente
                b_1 = sec[x_n.index(nueva[0])]
                b_2 = nueva
                end = True
        # Añado x_i a la lista de x anteriores        
        x_n.append(nueva[0])
        # Añado el nuevo elemento de la secuencia
        sec.append(nueva)
        # actualizo x_i con x_{i+1}
        sec_ant = nueva.copy()
    
    # Resolvemos la congruencia 
    return mt.congruencia(b_2[2]-b_1[2],b_1[1]-b_2[1],p-1)[1]

if __name__ == '__main__':
    a = 11
    b = 766
    p = 839
    print ("El log en base {} de {} mod {} usando fuerza bruta es: {}".format(a,b,p,log_bf(a,b,p)))
    print ("El log en base {} de {} mod {} usando el algoritmo paso pequeño-paso gigante es: {}".format(a,b,p,log_pe_pg(a,b,p)))
    print ("El log en base {} de {} mod {} usando el algoritmo rho de Pollard es: {}".format(a,b,p,log_ro_pollard(a,b,p)))