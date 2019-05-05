"""
Codigo que sirve como investigacion del problema de factorizacion
de un numero en n compuesto en primos mas pequeños con los cuales
podamos operar
"""
import util.primality as prim
from util.math import power_optimize, square, mcd
from math import ceil

def tentative (num):

    lista = list()
    
    while not prim.is_prime(num):
        prime = 2

        while (num % prime) != 0 and prime < num:
            prime = prim.next_prime(prime)
        
        if prime >= num:
            raise ArithmeticError ("Error detectanco la primalidad del numero")
        
        num = num // prime
        lista.append(prime)

    lista.append(num)
    return lista

def isSquare(num):
    sqnum = ceil(square(num))
    return (sqnum*sqnum) == num

def fermat (num):
    x = ceil(square(num))

    while not isSquare((x**2) - num):
        x += 1
    
    return (x, square((x**2) - num ))

def calculateSecuencia (lista, func = lambda x,n: ((x**2) + 1) % n ):

    x_i = lista[-1]

    for _ in range(len(lista), 2*len(lista)):
        x_i = func(x_i,num)
        lista.append(x_i)   

def pollard (num ,seed = 0, function = lambda x, n: ((x**2) + 1) % n ):

    i = 1
    x_i  = function(seed, num)
    lista = [ seed, x_i ]

    for _ in range(1, int(square(num) + 1)):
        x_i  = function(x_i, num)
        lista.append(x_i)
     
    while mcd( lista[i*2] - lista[i] , num) == 1:
        i += 1
        if i*2 >= len(lista):
            lista = calculateSecuencia(lista, function)
    
    return ( mcd( lista[i*2] - lista[i] , num), num // mcd( lista[i*2] - lista[i] , num) )


