# -*- coding: utf-8 -*-

import random
from cripto.util.math import power_optimize

minor_prime = [ 2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,
                131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,227,229,233,239,
                241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,
                389,397 ]

def basic_primality (num):

    """
    Autor : Ismael Marin Molina

    Control de primalidad para aquellos numeros factorizables por
    primos pequenos, para ello se itera sobre los primeros 50 primos
    y se va comprobando si alguno de ellos puede descomponer al numero dado

    Parameter
    --------------------

    num : Entero largo, numero el cual queremos comprobar su primalidad

    Return
    --------------------

    Si el valor es primo o no lo es
    """
    for elem in minor_prime:
        if (num % elem) == 0 and not elem == num:
            return False
    
    return True


def rabin_miller (num, iter = 5, tes = None, verbose = False):

    """
    Autor : Ismael Marin Molina

    Test de rabin miller para comprobar la primalidad de un numero, 
    inicialmente comprobamos si este numero es impar despues lo 
    descomponemos num - 1  como potencia de 2.

    Despues iteramos un numero de veces sacando numeros entre 2 y p - 2
    y vemos si son congruentes con el valor.

    Parameter
    ---------------------

    num : Entero, representando al numero
    iter : Entero, iteraciones 

    Returns
    ---------------------

    Verdadero si es primo falso en otro caso
    """    

    s = num - 1
    t = 0

    if num < 400:
        return basic_primality(num)
    elif num % 2 == 0:
        return False

    while s % 2 == 0:
        s = s // 2
        t += 1

    for _ in range(iter):
        if tes is None:
            a = random.randrange(2,num - 1)
        else:
            a = tes
        
        v = power_optimize(a,s,num)

        if v != 1 and v != num - 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    if (verbose):
                        print("Falla el test con a={} y u={}".format(a, s * (i+1) ))
                    return False
                elif v == 1:
                    if (verbose):
                        print("Falla el test con a={} y u={}".format(a, s * (i+1) ))
                    return False
                else:
                    i += 1
                    v = (v * v) % num

    return True 

def is_prime (num):
    """
    Author : Ismael Marin Molina

    Funcion para determinar si un numero introducido es
    primo o no lo es, para ello se usan la funciones de 
    rabin miller y un test de primalidad basico.

    Parameter
    --------------------------

    num : Entero, numero el cual vamos a determinar su primalidad

    Return
    --------------------------

    El resultado de basic_primality si es menor a 10000, si 
    no retorna el valor de rabin miller con 20 iteraciones
    """
    if num < 1000:
        return basic_primality(num)

    return rabin_miller(num, 20)

def next_prime_strong (num):
    """
    Author : Ismael Marin Molina

    Funcion para el calculo de primos fuertes, es decir 
    primos que cumplan que $ (num-1)/2 $ es tambien un 
    numero primo

    Parameter
    ----------------------------

    num : Entero, desde el cual se quiere empezar a calcular

    Return
    ---------------------------

    El siguiente primo fuerte desde el numero en el cual nos
    encontramos.
    """
    num = (num + 3) - (num % 4)

    k = next_prime( (num - 1) // 2 )

    while not is_prime( (2 * k) + 1 ):
        k = next_prime(k)
    
    return 2*k + 1

def next_prime (num):
    """
    Autor : Ismael Marin Molina

    Funcion para buscar elementos primos partiendo desde el 
    numero indicado, excluyendo estos numeros.

    Parameter
    ------------------------

    num : Entero, numero indicando desde donde empezar

    Return
    -------------------------

    el siguiente numero
    """
    num = num + 1 if (num % 2) == 0 else num + 2
    while not is_prime(num):
        num += 2
    return num
