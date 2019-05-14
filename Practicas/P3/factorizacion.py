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
    print("valor de x {}\tvalor de num {}".format(x, num))

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

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import time

    def number_compuest_of_n_bits (n):
        if n < 2:
            assert "Numero demasiado pequenio"
        
        primer_primo = prim.next_prime(2**(n//2))

        return primer_primo * prim.next_prime(primer_primo)
    
    def makes_times (numeros, funcion):
        times = list()
        len_n = list()
        stop = False
        stop_time = 12
        index = 0

        while not stop:
            start = time.time()
            funcion(numeros[index])
            end = time.time()

            times.append(end-start)
            len_n.append(len(bin(numeros[index])))

            index += 1

            print("Iteraccion {} con valor de tiempo {}".format(index, ( end-start )))

            if index >= len(numeros) or stop_time < (end - start):
                stop =  True
        
        print("Terminado con una cantidad de {}, y una longitud de {}".format(index, len_n[index-1]))
        
        return (times, len_n)

    numeros = [number_compuest_of_n_bits(n) for n in range(8,45) ]
    

    plt.title("Graficas")
    plt.subplot(3,1,1)
    plt.title("Tentativa")
    tiempos, tamanio = makes_times(numeros, tentative)
    plt.plot(tiempos, tamanio, 'o-')

    plt.subplot(3,1,2)
    plt.title("Fermat")
    tiempos, tamanio = makes_times(numeros, fermat)
    plt.plot(tiempos, tamanio, 'r-')

    plt.subplot(3,2,1)
    plt.title("Pollard")
    tiempos, tamanio = makes_times(numeros, pollard)
    plt.plot(tiempos, tamanio, 'b-')

    plt.show()



