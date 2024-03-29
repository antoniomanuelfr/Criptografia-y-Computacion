# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import random
import time

from math import sqrt, ceil
from random import randint

"""
" Funciones Proporcionadas
"""

#Calcula el máximo común divisor de dos números.
def mcd(a, b):
    while b != 0:
        (a, b) = (b, a % b)
    return a

#Calcula el inverso de a módulo b (si existe). Si ni existe, lo dice y devuelve 0.
def inversomodular(a, b):
    (u0, u1) = (1, 0)
    while b > 0:
        (u0, u1) = (u1, u0 - (a//b) * u1)
        (a, b) = (b, a%b)
    if a == 1:
        return u0
    else:
        print("No existe el inverso")
        return 0

#Resuelve la congruencia ax = b mod m. Da todas las soluciones comprendidas entre 0 y m-1.
def congruencia(a, b, m):
    d = mcd(a, m)
    if b%d == 0:
        n = m//d
        u = inversomodular(a//d, n)
        x = (u*(b//d))%n
        sol = []
        for i in range(d):
            sol.append(x)
            x = x+n
        return sol
    print("La congruencia no tiene solución")
    return([0])

#Calcula la raíz cuadrada entera de un número natural.
def raiz(n):
    m = (len(bin(n))-1) // 2
    x = 2**m
    y = (x**2+n)//(2*x)
    while x > y:
        (x, y) = (y, (y**2+n)//(2*y))
    return x

#Comprueba si un número natural es cuadrado perfecto.
def escuadrado(n):
    y = raiz(n)
    return(y**2 == n)

"""
" Funciones Utiles
"""

# Descompone s -> 2**u * s
def descomposicion(p):
    u, s = 0, p
    while (s % 2 == 0) and (s > 0):
        s = s // 2
        u += 1
    return u, s

# Calcula base**exponente % modulo
def potenciaModular(base, exponente, modulo):
    aux = 1
    while (exponente > 0):
        if (exponente%2 == 1):
            aux = (aux*base)%modulo
        exponente = exponente//2
        base = (base*base)%modulo
    return aux

# Validaciones del Test de Miller-Rabin
def MRvalidate(base, modulo, b):
    if (base == 1 or base == modulo-1):
        return True
    else:
        for i in range(1, b):
            base = (base*base)%modulo
            if (base == modulo-1):
                return True
            elif (base == 1):
                return False
    return False

# Funcion Test de Miller-Rabin
def testMillerRabin(p, n_testigos):
    b = 1
    if (p%2 != 0 and p >= 5):
        s = (p-1)//2
        while (s%2 == 0):
            s = s//2
            b += 1
        for i in range(0, n_testigos): 
            a = randint(2, p-2)
            a_1 = potenciaModular(a, s, p)
            result = MRvalidate(a_1, p, b)
            if (result == 0):
                return 0
        return 1
    else:
        return 0

def nextPrimo(m, n_testigos, fuerte = False):
    candidato = m
    if(candidato%2 == 0):
        candidato += 1
    else:
        candidato += 2
    if(fuerte == False):
        while ((testMillerRabin(candidato, n_testigos)) == 0):
            candidato += 2
        return candidato
    else:
        while True:
            if ((testMillerRabin(candidato, n_testigos)) == 1):
                if ((testMillerRabin((candidato-1)//2, n_testigos)) == 1):
                    break
            candidato += 2
        return candidato

def nextPrimoBits(m, n_testigos, writeInit = False, aleatorio = True):
    lowValor = 2**(m-1)+3
    highValor = 2**m
    if(aleatorio):
        candidato = randint(lowValor, highValor)
    else:
        candidato = lowValor
    while candidato < highValor:
        if ((testMillerRabin(candidato, n_testigos)) == 1):
            if(((testMillerRabin((candidato-1)//2, n_testigos)) == 1)):
                break
        candidato += 4
    if(writeInit == True):
        return candidato
    if(candidato >= highValor):
        print("No existe primo fuerte con los bits dados")
    else:
        return candidato

# Funcion Saber si es cuadrado perfecto
def cuadradoPerfecto(n):
    if n < 0:
        return False
    return sqrt(n).is_integer()

def factorizar(a, p):
    factores = []
    n = a
    if testMillerRabin(n, 10):
        return [n]
    if n % 2 == 0:
        factores.append(2)
        factores.append(n//2)
        return [2, n//2]
    a = ceil(sqrt(n))
    b2 = a**2 - n
    while not cuadradoPerfecto(b2):
        a += 1
        b2 = a**2 - n
    p = int(a - sqrt(b2))
    q = int(a + sqrt(b2))
    factores.append(p)
    factores.append(q)
    return [p, q]

"""
" Funciones de la Practica
"""

def simbolo_legendre(a, p):
    assert(p%2 != 0)
    assert(testMillerRabin(p, 10) == 1)
    assert(mcd(a, p) == 1)
    if (mcd(a, p) == 1):
        if (a == 1):
            return 1
        elif (a == -1):
            return int((-1)**((p-1)/2))
        elif (a == 2):
            return int((-1)**((p**2 - 1)/8))
        elif (cuadradoPerfecto(a)):
            return 1
        elif (a%p < a):
            return simbolo_legendre(a % p, p)
        elif (not testMillerRabin(a, 10)):
            b, c = factorizar(a, p)
            return simbolo_legendre(b, p) * simbolo_legendre(c, p)
        if (a%4 == 3) and (p%4 == 3):
            return -simbolo_legendre(p, a)
        else:
            return simbolo_legendre(p, a)
    else:
        return 0

def simbolo_jacobi(a, p):
    assert(p%2 != 0)
    if (p == 1):
        return 1
    if (a%2 == 0):
        aux = p%8
        if (aux == 7) or (aux == 1):
            return simbolo_jacobi(a//2, p)
        if (aux == 5) or (aux == 3):
            return -simbolo_jacobi(a//2, p)
    if (a%4 == 3) and (p%4 == 3):
        return -simbolo_jacobi(p%a, a)
    else:
        return simbolo_jacobi(p%a, a)
        
def algoritmo_tonelli(a, p):
    assert(p%2 != 0)
    assert(testMillerRabin(p, 10) == 1)
    assert(simbolo_jacobi(a, p) == 1)
    n = 2
    while (simbolo_jacobi(n, p) != -1):
        n += 1
    u, s = descomposicion(p-1)
    if (u == 1):
        return potenciaModular(a, (p+1)//4, p)
    r = potenciaModular(a, (s+1)//2, p)
    b = potenciaModular(n, s, p)
    c = potenciaModular(a, p-2, p)
    d = (c * r * r) % p
    for j in range(0, u-1):
        aux = potenciaModular(d, 2**(u-2-j), p)
        if (aux == p-1):
            r = (r * b) % p
            d = (d * b * b) % p
        b = (b * b) % p
    return r

"""
" Funciones de Prueba
"""

def prueba_legendre():
    print("Legendre -> (", 245, "/", 911, ") = ", simbolo_legendre(245, 911))
    print("Legendre -> (", 782, "/", 911, ") = ", simbolo_legendre(782, 911))

def prueba_jacobi():
    print("Jacobi -> (", 245, "/", 911, ") = ", simbolo_jacobi(245, 911))
    print("Jacobi -> (", 782, "/", 911, ") = ", simbolo_jacobi(782, 911))
            
def prueba_tonelli(seed = 20000913, showPrints = False, showResult = False, showGraphic = True):
    random.seed(seed)
    flag = 10
    vectorResult = []
    vectorP = []
    vectorTime = []
    for i in range(0, 100):
        p = nextPrimo(flag, 100)
        a = randint(2, p-1)
        while(simbolo_jacobi(a, p) != 1):
            a = randint(2, p-1)
        vectorP.append(len(str(p)))
        tIni = time.time()
        r = algoritmo_tonelli(a, p)
        tFin = time.time()
        finalTime = (tFin-tIni)*1000
        vectorTime.append(finalTime)
        result = ((r * r % p) == a)
        if (showPrints):
            print("Valor de a:", a)
            print("Valor de p:", p)
            print("Valor de r:", r)
            print("Es el Resultado Correcto?", result)
            print("Tiempo de Ejecucion:", finalTime, "\n")
        vectorResult.append(result)
        flag = flag * 1000
    if (showResult):
        print(vectorResult)
    if (showGraphic):
        plt.plot(vectorTime, vectorP)
        #plt.scatter(vectorTime, vectorP)
        plt.xlabel('Tiempo (Milisegundos)')
        plt.ylabel('Numero Primo')
        plt.title('Algoritmo de Tonelli')
        plt.show()

def main():
    #prueba_legendre()
    #prueba_jacobi()
    prueba_tonelli()
    
if __name__ == "__main__":
	main()