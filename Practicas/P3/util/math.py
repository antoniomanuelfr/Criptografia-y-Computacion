# -*- coding: utf-8 -*-
"""
Author: Ismael Marin Molina
Date : 11 - 04 - 19

La finalidad de este modulo es reunir diferentes operaciones recurrentes
que se usaran para el resto de utilidades.

python version: 3.7.1

"""

def power_optimize (a = 1, b = 0, c = 1):
    """
    Autor : Jesus Garcia Miranda

    Funcion para el calculo de la potencia de dos 
    numeros naturales en un anillo con valor c, para
    ello usamos las reglas de la multiplicacion
    modular, concretamente :

    $(a^b) mod c = ((a mod c) (a mod c) ... (a mod c)) mod c$

    Lanza una **ZeroDivisionError**, si se intenta realizar
    el modulo con c = 0

    Parameters
    ----------------------------------

    a : Entero, elemento potenciado
    b : Entero, exponente de la potencia
    c : Entero, elemento base del anillo

    Return
    ----------------------------------

    result : Entero, expresando el resultado
    """
    if c == 0:
        raise ZeroDivisionError("Error el valor de c no puede ser 0")

    result = 1

    while b > 0 :
        if (b % 2) == 1:
            result *= a 
            result = result % c
        
        b =  b // 2
        a = (a * a) % c

    return result


def square (n):
    """
    Autor : Jesus Garcia Miranda

    Funcion para el calculo mas preciso de la
    raiz cuadrada de un numero **n**, para ello
    tomamos el bit que se encuentre en la mitad mas
    uno como punto inicial y realizamos el metodo de 
    interpolacion de Newton-Rapson

    Parameter
    ----------------------------

    n : Entero, numero al cual vamos a calcular la raiz

    Return
    ----------------------------

    x : El valor de la raiz cuadrada entera del elemento
    """
    if isinstance(n, float):
        raise ValueError("Error valor no permitido")
        
    if n == 0:
        return 0


    i = 0
    m = len( bin(n) ) // 2

    x = 2**m
    y = (x**2 + n) // (2*x)

    while x > y:
        x = y
        y = (x**2 + n) // (2*x)
        i += i
    
    return x

def mcd(a,b):
    """
    Autor : Jesus García Miranda

    Calcula el maximo comun divisor de los 
    numeros pasados como argumentos

    Parameter
    --------------------------

    a : Entero con el valor primario
    b : Entero con el valor secundario

    Return
    --------------------------

    a : Entero representando el maximo comun divisor
    """
    while b!=0:
        (a,b) = (b,a%b)
    return a

def inversomodular(a,b):
    """
    Autor : Jesus García Miranda

    Funcion para calcular el inverso de un numero
    en un cuerpo de valor p.

    Exception : NOSOLUTION

    Parameter
    ------------------------

    a : Numero al cual buscar el inverso
    b : Modularidad

    Return 
    -------------------------

    u0 : Inverso del numero
    """
    (u0,u1) = (1,0)
    while b>0:
       (u0,u1) = (u1,u0-(a//b)*u1)
       (a,b) = (b,a%b)
    if a == 1:
       return u0
    else:
       raise ArithmeticError("No solution in inverse function")
       return 0

def mcd_ex (a,b):
    (u0,u1)=(1,0)
    (v0,v1)=(0,1)
    while b > 0:
        (c,r) = (a//b, a%b)
        (u0,u1) = (u1,u0-c*u1)
        (v0,v1) = (v1,v0-c*v1)
        (a,b) = (b, a%b)
    return [a,u0,v0]

def congruencia(a,b,m):
    """
    Autor : Jesus García Miranda

    Funcion para calcular las soluciones a la congruencia
    ax = b mod m

    Exception : NOSOLUTION

    Parameter
    ------------------------

    a : Numero al cual buscar el inverso
    b : Modularidad

    Return 
    -------------------------

    u0 : Inverso del numero
    """
<<<<<<< Updated upstream
    d = mcd(a,m)
    if b%d == 0:
       n = m//d
       u = inversomodular(a//d,n)
       x = (u*(b//d))%n
       sol = []
       for i in range(d):
           sol.append(x)
           x = x+n
       return sol
    return([0])
=======
    d = mcd_ex(a,m)
    if b%d[0] == 0:
       n = m//d[0]
       x = (d[1]*(b//d[0]))%n
       return [n,x]
    raise ArithmeticError("No solution in congruence function")
    return([0,0])

def sistema (l):
    sol = [0,1]
    for y in l:
        z = congruencia(y[0]*sol[1],(y[1]-y[0]*sol[0])%y[2],y[2])
        sol = [sol[0]+sol[1]*z[0],sol[1]*z[1]]
    return(sol)
>>>>>>> Stashed changes
