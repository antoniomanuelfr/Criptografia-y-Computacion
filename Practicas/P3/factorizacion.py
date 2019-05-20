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
    x = square(num) + 1

    while not isSquare((x**2) - num):
        x += 1
    
    return ( x - square((x**2) - num ), x + square((x**2) - num ) )

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
    import random

    def near_comp_number (n):
        if n < 2:
            assert "Numero demasiado pequenio"
        
        num = random.randrange(2**n, 2**(n+1))

        primer_primo = prim.next_prime(num)

        return primer_primo * prim.next_prime(primer_primo)
    
    def random_simple_number (inf, sup):
        prime1, prime2 = prim.next_prime(random.randrange(inf,sup)), prim.next_prime(random.randrange(inf,sup))
        return prime1 * prime2

    def makes_times (numeros, funcion):
        times = list()
        len_n = list()
        stop = False
        stop_time = 20
        index = 0

        while not stop:
            start = time.time()
            n1,n2 = funcion(numeros[index])
            end = time.time()

            times.append(end-start)
            len_n.append(len(bin(numeros[index])) - 2)

            print("Numero compuesto de {} bits, tiempo de factorizacion: {}".format( len(bin(numeros[index])) - 2 , ( end-start )))

            if n1*n2 != numeros[index]:
                print("Failed with {}, resultado: {}x{}".format(numeros[index], n1, n2))
                stop = True

            index += 1

            if index >= len(numeros) or stop_time < (end - start):
                stop =  True
        
        print("Aniadidos {}, cantidad de bits del ultimo numero analizado {}".format(index, len_n[index-1]))
        
        return (times, len_n)
    
    def make_time_mean(numeros, funcion):
        times = list()
        means = list()
        stop = False
        stop_time = 100
        index = 0
        aux = 0

        while not stop:
            start = time.time()
            n1,n2 = funcion(numeros[index])
            end = time.time()

            aux += end-start

            times.append(end-start)
            means.append(aux / len(times))

            print("Media actual {}, tiempo de factorizacion: {}".format( aux / len(times) , ( end-start )))

            if n1*n2 != numeros[index]:
                print("Failed with {}, resultado: {}x{}".format(numeros[index], n1, n2))
                stop = True

            index += 1

            if index >= len(numeros) or stop_time < (end - start):
                stop =  True
        
        print("Aniadidos {}, media final {}".format(index, means[index-1]))
        
        return (times, means)
    
    def advantage_tentative (bits):
        bits_square = square(bits) if bits < 14 else 7
        sup = bits - bits_square

        p = random.randrange(2**bits_square, 2**(bits_square+1))
        n = random.randrange(2**sup,2**(sup+1))

        return prim.next_prime( p ) * prim.next_prime( n )

    numeros = [advantage_tentative(i) for i in range(4,45) ]    

    plt.title("Tentativa vs Fermat vs Pollard")
    tiempos, media = makes_times(numeros, tentative)
    plt.plot(range(len(tiempos)), tiempos, 'b-', label="Tentativa")
    #plt.plot(range(len(tiempos)), media, '-' ,alpha=0.7 , label="Media tentativa")

    tiempos, media = makes_times(numeros, fermat)
    plt.plot(range(len(tiempos)), tiempos, 'r-', label="Fermat")
    #plt.plot(range(len(tiempos)), media, '-' ,alpha=0.7 , label="Media Fermat")

    tiempos, media = makes_times(numeros, pollard)
    plt.plot(range(len(tiempos)), tiempos, 'g-', label="Pollard")
    #plt.plot(range(len(tiempos)), media, '-' ,alpha=0.7 , label="Media Pollard")

    plt.legend()
    plt.show()



