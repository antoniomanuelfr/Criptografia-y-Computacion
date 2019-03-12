import random


# random.seed(9)


# def potencias(a, b, m):
#     if m == 0:
#         return -1
#     aux = a
#     for i in range(b - 1):
#         aux = (aux * a) % m
#
#     return aux

# def func3(n):
#     res = []
#     for i in range(n):
#         if potencia_modular(i, 2, n) == 1:
#             res.append(i)
#     return res


def potencia_modular(x, y, z):
    aux = 1
    while y > 0:
        if y % 2 == 1:
            aux = (aux * x) % z
        x *= x
        y = y // 2
        x %= z
    return aux


def descomponer(a):
    cont = 0
    b = a
    while b % 2 == 0:
        cont = cont + 1
        b = b // 2
    return cont, b


def miller_rabin(p, ft=None, pr=False):
    if p >= 5 and p % 2 == 1:
        u, s = descomponer(p - 1)

        testigo_actual = random.randint(2, p - 2) if ft is None else ft

        if pr:
            print("Estamos usando como testigo: a = ", testigo_actual)

        res = potencia_modular(testigo_actual, s, p)

        if pr:
            print("{} ^ {} = {} mod {}".format(res, s, res, p))

        if res == 1 or res == p - 1:
            return True

        for i in range(1, u):
            res = potencia_modular(res, 2, p)
            if pr:
                print("{} ^ {} = {} mod {}".format(res, s * (2 ** i), res, p))
            if res == p - 1:
                return True
            elif res == 1:
                return False

    return False


def buscar_todos_falsos_testigos(p, pr=False):
    falsos_testigos = []

    if p >= 5 and p % 2 == 1:
        u, s = descomponer(p - 1)
        for a in range(2, p - 2):

            res = potencia_modular(a, s, p)

            if res == 1 or res == p - 1:
                falsos_testigos.append(a)

            else:

                if pr:
                    print("{} ^ {} = {} mod {}".format(res, s, res, p))

                for i in range(1, u):
                    res = potencia_modular(res, 2, p)
                    if pr:
                        print("{} ^ {} = {} mod {}".format(res, s * (2 ** i), res, p))

                    if res == p - 1:
                        falsos_testigos.append(a)
                    elif res == 1:
                        break

    return falsos_testigos


def es_primo(p, testigo=None, n=10, pr=False):
    for i in range(n):

        if not miller_rabin(p=p, ft=testigo, pr=pr):

            if pr:
                print(p, " no es primo\n")

            return False
    if pr:
        print(p, " es posible primo\n")

    return True


def siguiente_primo(p):
    aux = p + 1 if p % 2 == 0 else p + 2

    while not miller_rabin(p=aux, ft=None, pr=False):
        aux += 2
    return aux


def primo_fuerte_n_bits(n):
    sem = random.randint(2 ** (n - 1), 2 ** n)

    primo = primo_fuerte(sem)
    cont = 0
    while primo > 2 ** n:
        print("{} es mayor que 2^{} con la semilla {}".format(primo, n, sem))

        sem = random.randint(2 ** (n - 1), 2 ** n)
        primo = primo_fuerte(sem)

        cont += 1
        if cont == 10:
            break

    return primo


# n > 4 bits
def primo_fuerte(n):
    prmo = siguiente_primo(n)
    while not es_primo((prmo - 1) // 2):
        prmo = siguiente_primo(prmo)

    return prmo


if __name__ == '__main__':

    prueba = 561
    # Apartado 1
    es_primo(p=prueba, testigo=None, n=10, pr=True)

    # Apartado 2
    testigo_prueba = 101
    es_primo(p=prueba, testigo=testigo_prueba, n=1, pr=True)
    print("Los falsos testigos de {} son: \n{}\n".format(prueba, buscar_todos_falsos_testigos(prueba, pr=False)))

    # Apartado 3
    print("El siguiente primo a {} es: {}".format(prueba, siguiente_primo(prueba)))

    # Apartado 4
    print("El siguiente primo fuerte a {} es: {}".format(prueba, primo_fuerte(prueba)))

    # Apartado 5
    n_bits = 8
    print("Un primo fuerte de {} bits es: {}".format(n_bits, primo_fuerte_n_bits(n_bits)))

    # Apartado 6
    lista_pruebas = [6601, 8911, 10585, 15841, 29341]
    for pruebas in lista_pruebas:
        print("Los falsos testigos de {} son: \n{}\n".format(pruebas, buscar_todos_falsos_testigos(pruebas, pr=False)))

    # Apartado 7